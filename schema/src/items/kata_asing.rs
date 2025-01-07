//! Contains struct [KataAsing] which map a foreign word with its language of origin.

/// Contains a foreign word with its language of origin.
#[derive(Clone, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct KataAsing {
    pub nama: String,
    pub bahasa: String,
}

impl KataAsing {
    pub fn null() -> Self {
        Self {
            nama: "".into(),
            bahasa: "".into(),
        }
    }
}
