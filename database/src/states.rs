//! Connections to database

use sqlx::migrate::MigrateDatabase;
use sqlx::migrate::{Migrate, MigrateError};
use sqlx::FromRow;

use crate::errors::Result;
use crate::prelude::BackendError;

// TODO: Refactor this module

/// Connection to database
#[derive(Debug, Clone)]
pub struct Connection<DB: sqlx::Database> {
    #[allow(missing_docs)]
    pub pool: sqlx::Pool<DB>,
}

/// Counts of selected items.
#[allow(missing_docs)]
#[derive(Debug, Clone, Default, serde::Serialize, PartialEq, ts_rs::TS)]
#[ts(export, export_to = "../../src/bindings/")]
pub struct Counts<I> {
    lemmas: I,
    konseps: I,
    golongan_katas: I,
    cakupans: I,
    kata_asings: I,
}

/// A helper struct for when a single string value is queried.
pub struct StringItem {
    #[allow(missing_docs)]
    pub item: String,
}

impl Counts<Option<i64>> {
    fn unwrap_fields(self) -> Counts<i64> {
        Counts {
            lemmas: self.lemmas.unwrap_or(0),
            konseps: self.konseps.unwrap_or(0),
            golongan_katas: self.golongan_katas.unwrap_or(0),
            cakupans: self.cakupans.unwrap_or(0),
            kata_asings: self.kata_asings.unwrap_or(0),
        }
    }
}

#[cfg(feature = "postgres")]
impl Connection<sqlx::Postgres> {
    pub async fn from(url: String) -> Self {
        Self {
            pool: sqlx::PgPool::connect(&url).await.unwrap(),
        }
    }
    /// Queries the counts of each items as [Counts].
    ///
    /// The function calls the following query:
    /// ```sql
    #[doc = include_str!("../transactions/postgres/count_items.sql")]
    /// ```
    pub async fn statistics(self) -> Result<Counts<i64>> {
        let inter: Counts<Option<i64>> =
            sqlx::query_file_as!(Counts, "transactions/postgres/count_items.sql")
                .fetch_one(&self.pool)
                .await
                .map_err(BackendError::from)?;
        Ok(inter.unwrap_fields())
    }
}

#[cfg(feature = "sqlite")]
impl Connection<sqlx::Sqlite> {
    /// Forcefully reconnect to the specified url.
    pub async fn renew(&mut self, url: String) -> Result<&Self> {
        self.pool = sqlx::SqlitePool::connect(&url).await?;
        Ok(self)
    }

    /// Acquires a connection to the specified url.
    ///
    /// If not exist, creates and applies [Self::create_and_migrate] to the same url.
    pub async fn from(url: String) -> Self {
        match sqlx::SqlitePool::connect(&url).await {
            Ok(pool) => {
                // Automatically migrate to current version
                Self { pool }
            }
            Err(_) => {
                let _ = Self::create_and_migrate(url.clone())
                    .await
                    .unwrap()
                    .populate_with_presets()
                    .await
                    .unwrap();
                Connection::from(url).await
            }
        }
    }

    /// Queries the counts of each items as [Counts].
    ///
    /// The function calls the following query:
    /// ```sql
    #[doc = include_str!("../transactions/sqlite/count_items.sql")]
    /// ```
    pub async fn statistics(self) -> Result<Counts<i32>> {
        sqlx::query_file_as!(Counts, "transactions/sqlite/count_items.sql")
            .fetch_one(&self.pool)
            .await
            .map_err(BackendError::from)
    }

    /// Queries all `golongan_kata.nama` and returns Result<Vec<[StringItem]>>
    ///
    /// The function calls the following query:
    /// ```sql
    /// SELECT nama AS item FROM golongan_kata
    /// ```
    pub async fn get_golongan_kata_enumeration(self) -> Result<Vec<StringItem>> {
        sqlx::query_as!(StringItem, "SELECT nama AS item FROM golongan_kata")
            .fetch_all(&self.pool)
            .await
            .map_err(BackendError::from)
    }

    /// Creates the Sqlite database in the specified url then apply migrations.
    pub async fn create_and_migrate(url: String) -> Result<Self> {
        sqlx::Sqlite::create_database(&url).await?;
        let pool = sqlx::SqlitePool::connect(&url).await?;
        Ok(Self::migrate(pool).await)
    }

    async fn migrate(pool: sqlx::Pool<sqlx::Sqlite>) -> Self {
        match sqlx::migrate!("migrations/sqlite").run(&pool).await {
            Ok(_) => Self { pool },
            // Err(MigrateError::VersionMismatch(v)) => {println!("{}", v);  Self{pool}}
            Err(e) => todo!("{}", e),
        }
    }

    /// Populates the database with presets to satisfy certain constrains.
    ///
    /// The current constrain is that the `konsep.golongan_kata` field must point to a `golongan_kata.id`.
    /// This function calls the following query:
    /// ```sql
    #[doc = include_str!("../presets/golongan_kata_ms-my.sql")]
    /// ```
    pub async fn populate_with_presets(&self) -> Result<&Self> {
        sqlx::query_file!("presets/golongan_kata_ms-my.sql")
            .execute(&self.pool)
            .await?;
        Ok(self)
    }
}
