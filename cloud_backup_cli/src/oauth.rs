use reqwest::blocking::Client;
use serde::Deserialize;
use std::collections::HashMap;
use urlencoding::encode;

#[derive(Deserialize, Debug)]
pub struct TokenResponse {
    pub access_token: String,
    pub refresh_token: Option<String>,
    pub expires_in: Option<i64>,
}

pub fn build_authorize_url(client_id: &str, redirect: &str) -> String {
    // ВАЖНО: scope НЕ передаём, Яндекс сам выдаст права,
    // которые ты выбрал в настройках приложения (Яндекс.Диск REST API).
    format!(
        "https://oauth.yandex.ru/authorize?response_type=code&client_id={}&redirect_uri={}",
        client_id,
        encode(redirect),
    )
}

pub fn exchange_code_for_token(
    client_id: &str,
    client_secret: &str,
    code: &str,
    redirect: &str,
) -> Result<TokenResponse, Box<dyn std::error::Error>> {
    let client = Client::new();
    let url = "https://oauth.yandex.ru/token";

    let mut params: HashMap<&str, &str> = HashMap::new();
    params.insert("grant_type", "authorization_code");
    params.insert("code", code);
    params.insert("client_id", client_id);
    params.insert("client_secret", client_secret);
    params.insert("redirect_uri", redirect);

    let resp = client.post(url).form(&params).send()?;

    if !resp.status().is_success() {
        let s = resp.status();
        let txt = resp.text().unwrap_or_default();
        return Err(format!("Token request failed: {} — {}", s, txt).into());
    }

    let token_resp: TokenResponse = resp.json()?;
    Ok(token_resp)
}
