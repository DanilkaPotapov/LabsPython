use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct OAuthConfig {
    pub client_id: String,
    pub client_secret: String,
    pub redirect_uri: String,
}

#[derive(Debug, Deserialize)]
pub struct Settings {
    pub source_dir: String,
    pub backup_dir: Option<String>,
    pub enabled: bool,
    pub oauth: OAuthConfig,
    pub scopes: Option<String>,
}

impl Settings {
    pub fn new() -> Result<Self, config::ConfigError> {
        let settings = config::Config::builder()
            .add_source(config::File::with_name("config/default"))
            .build()?;

        settings.try_deserialize()
    }
}
