use std::fs::{self, File};
use std::io::{Read, Write}; // <-- FIX здесь
use std::path::Path;

use walkdir::WalkDir;
use zip::write::FileOptions;
use zip::CompressionMethod;

pub fn create_backup_archive(
    source_dir: &str,
    backup_dir_opt: Option<String>,
) -> Result<String, Box<dyn std::error::Error>> {
    let backup_dir = backup_dir_opt.unwrap_or("./backups".to_string());

    fs::create_dir_all(&backup_dir)?;

    let timestamp = chrono::Local::now().format("%Y%m%d_%H%M%S").to_string();
    let archive_name = format!("backup_{}.zip", timestamp);
    let archive_path = Path::new(&backup_dir).join(&archive_name);

    let file = File::create(&archive_path)?;
    let mut zip = zip::ZipWriter::new(file);

    let options = FileOptions::default()
        .compression_method(CompressionMethod::Deflated)
        .unix_permissions(0o644);

    let src_path = Path::new(source_dir);
    if !src_path.exists() {
        return Err(format!("Source '{}' not found", source_dir).into());
    }

    for entry in WalkDir::new(src_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let name = path.strip_prefix(src_path)?.to_string_lossy();

        if path.is_file() {
            let zip_path = name.replace("\\", "/");
            zip.start_file(zip_path, options)?;
            let mut f = File::open(path)?;
            let mut buf = Vec::new();
            f.read_to_end(&mut buf)?;
            zip.write_all(&buf)?; // <- FIX WORKING
        } else if path.is_dir() {
            let dir_name = if name.is_empty() {
                ".".to_string()
            } else {
                format!("{}/", name.replace("\\", "/"))
            };
            zip.add_directory(dir_name, options)?;
        }
    }

    zip.finish()?;
    Ok(archive_path.to_string_lossy().to_string())
}
