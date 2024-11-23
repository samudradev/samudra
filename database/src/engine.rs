use crate::io::interface::View;
use crate::views::LemmaWithKonsepView;
use sqlx::Error::Database;
use sqlx::Executor;

pub struct DbEngine<P: SqlxPool> {
    inner: P,
}

impl<P: SqlxPool> DbEngine<P> {
    pub(crate) fn pool(&self) -> &P {
        &self.inner
    }
}

pub trait SqlxPool: Send + Unpin {
    type DB;
}

#[async_trait::async_trait]
pub trait Query<V: View> {
    type ViewOption;

    async fn select(&self, option: Self::ViewOption) -> sqlx::Result<Vec<V>>;
}

pub struct LemmaWithKonsepViewOption {
    pub lemma: Option<String>,
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl Query<LemmaWithKonsepView> for DbEngine<sqlx::SqlitePool> {
    type ViewOption = LemmaWithKonsepViewOption;

    async fn select(&self, option: Self::ViewOption) -> sqlx::Result<Vec<LemmaWithKonsepView>> {
        sqlx::query_file_as!(
            LemmaWithKonsepView,
            "transactions/select_lemma_with_konsep_view.sql",
            option.lemma
        )
        .fetch_all(&self.inner)
        .await
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl Query<LemmaWithKonsepView> for DbEngine<sqlx::PgPool> {
    type ViewOption = LemmaWithKonsepViewOption;

    async fn select(&self, option: Self::ViewOption) -> sqlx::Result<Vec<LemmaWithKonsepView>> {
        sqlx::query_file_as!(
            LemmaWithKonsepView,
            "transactions/select_lemma_with_konsep_view.sql",
            option.lemma
        )
        .fetch_all(&self.inner)
        .await
    }
}

#[cfg(feature = "sqlite")]
impl SqlxPool for sqlx::SqlitePool {
    type DB = sqlx::Sqlite;
}

#[cfg(feature = "sqlite")]
impl DbEngine<sqlx::SqlitePool> {
    pub async fn sqlite(url: &str) -> Self {
        DbEngine {
            inner: sqlx::SqlitePool::connect(url)
                .await
                .expect("Sqlite connection error"),
        }
    }
}

#[cfg(feature = "postgres")]
impl SqlxPool for sqlx::PgPool {
    type DB = sqlx::Postgres;
}

#[cfg(feature = "postgres")]
impl DbEngine<sqlx::PgPool> {
    pub async fn postgres(url: &str) -> Self {
        DbEngine {
            inner: sqlx::PgPool::connect(url)
                .await
                .expect("Pg connection error"),
        }
    }
}
