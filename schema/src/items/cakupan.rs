/// The context in which a word with the corresponding definition is used.
#[derive(Clone, PartialEq, Hash, Eq, serde::Serialize, serde::Deserialize)]
pub struct Cakupan(String);

impl Cakupan {
    pub fn null() -> Self {
        Self("".into())
    }

    pub fn value(&self) -> String {
        self.0.clone().to_owned()
    }

    pub fn to_string(self) -> String {
        self.0
    }

    pub fn new(value: String) -> Self {
        Self(value)
    }
}

impl From<&str> for Cakupan {
    fn from(value: &str) -> Self {
        Self::new(value.into())
    }
}
impl From<String> for Cakupan {
    fn from(value: String) -> Self {
        Self::new(value)
    }
}
