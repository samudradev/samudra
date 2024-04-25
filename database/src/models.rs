pub mod cakupan;
pub mod cakupan_x_konsep;
pub mod golongan_kata;
pub mod kata_asing;
pub mod kata_asing_x_konsep;
pub mod konsep;
pub mod lemma;

#[async_trait::async_trait]
pub(crate) trait JointTable<DB>: ormlite::Model<DB>
where
    DB: sqlx::Database,
{
    async fn insert_safe(self, pool: &sqlx::Pool<DB>) -> sqlx::Result<Self> {
        Ok(self
            .insert(pool)
            .on_conflict(ormlite::query_builder::OnConflict::Ignore)
            .model)
    }
}
