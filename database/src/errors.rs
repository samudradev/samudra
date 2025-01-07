//! Custom error types.

use std::{error::Error, fmt::Display};

pub(crate) type Result<T> = std::result::Result<T, BackendError>;

#[derive(Debug)]
pub struct BackendError {
    pub message: String,
}

impl sqlx::error::DatabaseError for BackendError {
    fn message(&self) -> &str {
        &self.message
    }

    fn as_error(&self) -> &(dyn Error + Send + Sync + 'static) {
        todo!("LOW PRIORITY")
    }

    fn as_error_mut(&mut self) -> &mut (dyn Error + Send + Sync + 'static) {
        todo!("LOW PRIORITY")
    }

    fn into_error(self: Box<Self>) -> Box<dyn Error + Send + Sync + 'static> {
        todo!("LOW PRIORITY")
    }

    fn kind(&self) -> sqlx::error::ErrorKind {
        todo!("LOW PRIORITY")
    }
}

impl Error for BackendError {}
impl Display for BackendError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&format!("Backend Error: {}", &self.message))
    }
}

impl From<sqlx::Error> for BackendError {
    fn from(value: sqlx::Error) -> Self {
        BackendError {
            message: value.to_string(),
        }
    }
}

impl From<sqlx::migrate::MigrateError> for BackendError {
    fn from(value: sqlx::migrate::MigrateError) -> Self {
        BackendError {
            message: value.to_string(),
        }
    }
}
