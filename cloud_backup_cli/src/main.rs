mod backup;
mod config;
mod oauth;
mod uploader;

use crate::config::Settings;
use clap::{Parser, Subcommand};
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;
use std::thread;
use std::time::Duration;

use serde::{Deserialize, Serialize};

#[derive(Parser)]
#[command(version, about = "cloud_backup — zip + upload to Yandex.Disk")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Auth,
    Run,
    Status,
}

#[derive(Serialize, Deserialize, Debug)]
struct Tokens {
    access_token: String,
    refresh_token: Option<String>,
    expires_in: Option<i64>,
}

fn tokens_path() -> PathBuf {
    PathBuf::from("config/tokens.json")
}

fn save_tokens(tokens: &Tokens) -> Result<(), Box<dyn std::error::Error>> {
    let p = tokens_path();
    fs::create_dir_all(p.parent().unwrap())?;
    let s = serde_json::to_string_pretty(tokens)?;
    fs::write(p, s)?;
    Ok(())
}

fn load_tokens() -> Option<Tokens> {
    let p = tokens_path();
    let data = fs::read_to_string(p).ok()?;
    serde_json::from_str(&data).ok()
}

fn main() {
    let cli = Cli::parse();
    let settings = Settings::new().expect("Failed to read config/default.toml");

    match cli.command {
        Commands::Auth => {
            println!("=== OAuth authorization ===");
            let client_id = settings.oauth.client_id;
            let client_secret = settings.oauth.client_secret;
            let redirect = settings.oauth.redirect_uri;

            let url = oauth::build_authorize_url(&client_id, &redirect);
            println!(
                "Open this URL in your browser and authorize the application:\n\n{}\n",
                url
            );
            println!("After authorization you'll see a code (verification code). Paste it here:");

            print!("Code: ");
            io::stdout().flush().unwrap();
            let mut code = String::new();
            io::stdin().read_line(&mut code).unwrap();
            let code = code.trim();

            match oauth::exchange_code_for_token(&client_id, &client_secret, code, &redirect) {
                Ok(tr) => {
                    println!("Access token received. Saving to config/tokens.json");
                    let tokens = Tokens {
                        access_token: tr.access_token,
                        refresh_token: tr.refresh_token,
                        expires_in: tr.expires_in,
                    };
                    if let Err(e) = save_tokens(&tokens) {
                        eprintln!("Failed to save tokens: {}", e);
                    } else {
                        println!("Saved.");
                    }
                }
                Err(e) => {
                    eprintln!("Failed to exchange code for token: {}", e);
                }
            }
        }

        Commands::Run => {
            let tokens = match load_tokens() {
                Some(t) => t,
                None => {
                    eprintln!("No tokens found. Run `cloud_backup auth` first.");
                    return;
                }
            };

            println!("Creating archive from: {}", settings.source_dir);
            match backup::create_backup_archive(&settings.source_dir, settings.backup_dir.clone()) {
                Ok(archive_path_str) => {
                    println!("Archive created: {}", archive_path_str);

                    let file_name = PathBuf::from(&archive_path_str)
                        .file_name()
                        .unwrap()
                        .to_string_lossy()
                        .to_string();

                    // было:
                    // let remote_path = format!("backups/{}", file_name);

                    // стало:
                    let remote_path = file_name.clone();

                    let access_token = tokens.access_token.clone();
                    let archive_path = PathBuf::from(archive_path_str.clone());

                    println!("Uploading {} -> {}", archive_path.display(), remote_path);

                    // синхронная загрузка, ждем окончания
                    match uploader::upload_file_to_yandex(
                        &access_token,
                        &archive_path,
                        &remote_path,
                    ) {
                        Ok(()) => println!("Upload finished: {}", archive_path.display()),
                        Err(e) => eprintln!("Upload error: {}", e),
                    }
                }
                Err(e) => {
                    eprintln!("Failed to create archive: {}", e);
                }
            }
        }

        Commands::Status => {
            let dir = settings.backup_dir.unwrap_or("./backups".to_string());
            println!("Backups in {}", dir);

            match std::fs::read_dir(&dir) {
                Ok(entries) => {
                    let mut items: Vec<_> = entries.filter_map(|e| e.ok()).collect();
                    items.sort_by_key(|e| {
                        e.metadata()
                            .and_then(|m| m.modified())
                            .unwrap_or(std::time::SystemTime::UNIX_EPOCH)
                    });
                    items.reverse();

                    for (i, entry) in items.iter().take(20).enumerate() {
                        let p = entry.path();
                        let size = entry.metadata().map(|m| m.len()).unwrap_or(0);
                        println!("{}: {} ({} bytes)", i + 1, p.display(), size);
                    }
                }
                Err(e) => eprintln!("Error reading backup_dir: {}", e),
            }
        }
    }
}
