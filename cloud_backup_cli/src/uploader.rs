use std::fs::File;
use std::path::Path;

use reqwest::blocking::{Body, Client};
use reqwest::header::AUTHORIZATION;
use serde::Deserialize;
use urlencoding::encode;

#[derive(Deserialize)]
struct UploadHrefResponse {
    href: String,
}

pub fn get_upload_href(
    token: &str,
    remote_path: &str,
) -> Result<String, Box<dyn std::error::Error>> {
    let api = format!(
        "https://cloud-api.yandex.net/v1/disk/resources/upload?path={}&overwrite=true",
        encode(remote_path)
    );

    let resp = Client::new()
        .get(&api)
        .header(AUTHORIZATION, format!("OAuth {}", token))
        .send()?;

    if !resp.status().is_success() {
        return Err(format!("Error: {}", resp.text()?).into());
    }

    let json: UploadHrefResponse = resp.json()?;
    Ok(json.href)
}

pub fn upload_file_to_yandex(
    token: &str,
    local_path: &Path,
    remote_path: &str,
) -> Result<(), Box<dyn std::error::Error>> {
    let url = get_upload_href(token, remote_path)?;

    let file = File::open(local_path)?;
    let size = file.metadata()?.len();

    let resp = Client::new()
        .put(&url)
        .body(Body::sized(file, size))
        .send()?;

    if !resp.status().is_success() {
        return Err(format!("Upload failed: {}", resp.text()?).into());
    }

    Ok(())
}
