//! Contains the [CakupanItem].

use crate::io::interface::{AttachmentItemMod, FromView, Item, ItemMod, SubmitItem};
use crate::prelude::*;
use crate::states::{Pool, Sqlite};
use tracing::instrument;

/// The context in which a word with the corresponding definition is used.
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, Hash, Eq)]
pub struct CakupanItem(String);

impl ItemMod for CakupanItem {
    type FromItem = CakupanItem;

    fn from_item(value: &Self::FromItem) -> Self {
        value.clone()
    }
}

impl CakupanItem {
    pub fn null() -> Self {
        CakupanItem("".into())
    }

    pub fn to_string(self) -> String {
        self.0
    }
}

impl Item for CakupanItem {
    type IntoMod = CakupanItem;

    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        Ok(other.clone())
    }

    fn partial_from_mod(other: &Self::IntoMod) -> Self {
        CakupanItem(other.0.clone())
    }
}

impl FromView for CakupanItem {
    type VIEW = LemmaWithKonsepView;

    fn from_views(value: &Vec<Self::VIEW>) -> Vec<Self> {
        value
            .clone()
            .into_iter()
            .filter(|a| a.cakupan.is_some())
            .into_group_map_by(|a| a.cakupan.clone().expect("None have been filtered out"))
            .keys()
            .map(|a| Self::from(a.to_owned()))
            .collect_vec()
    }
}

impl From<&str> for CakupanItem {
    fn from(value: &str) -> Self {
        Self(value.into())
    }
}
impl From<String> for CakupanItem {
    fn from(value: String) -> Self {
        Self(value)
    }
}

// #[async_trait::async_trait]
// impl SubmitItem<sqlx::Sqlite> for CakupanItem {
//     async fn submit_full(&self, pool: &sqlx::Pool<sqlx::Sqlite>) -> sqlx::Result<()> {
//         sqlx::query! {
//             r#"INSERT or IGNORE INTO cakupan (nama) VALUES (?)"#,
//             self.0
//         }
//         .execute(pool)
//         .await?;
//         Ok(())
//     }
//
//     async fn submit_partial(&self, pool: &Pool<Sqlite>) -> sqlx::Result<()> {
//         self.submit_full(pool).await
//     }
//
//     async fn submit_full_removal(&self, _pool: &Pool<Sqlite>) -> sqlx::Result<()> {
//         todo!()
//     }
//
//     async fn submit_partial_removal(&self, _pool: &Pool<Sqlite>) -> sqlx::Result<()> {
//         todo!()
//     }
// }

#[async_trait::async_trait]
impl AttachmentItemMod<KonsepItem, sqlx::Sqlite> for CakupanItem {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &KonsepItem,
        pool: &sqlx::Pool<sqlx::Sqlite>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Attaching <Cakupan={}> to <{}:{}>",
            self.0,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
                r#"
                INSERT or IGNORE INTO cakupan (nama) VALUES (?);
                INSERT or IGNORE INTO cakupan_x_konsep (cakupan_id, konsep_id)
                    VALUES (
                        (SELECT id FROM cakupan WHERE cakupan.nama = ?),
                        (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                    );"#,
            self.0,
            self.0,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error attaching cakupan to konsep");
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &KonsepItem,
        pool: &sqlx::Pool<sqlx::Sqlite>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Detaching <Cakupan={}> from <{}:{}>",
            self.0,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
            r#" DELETE FROM cakupan_x_konsep AS cxk
                WHERE (
                    cxk.cakupan_id = (SELECT id FROM cakupan WHERE cakupan.nama = ?)
                        AND
                    cxk.konsep_id = (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                );"#,
            self.0,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error detaching cakupan from konsep");
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &KonsepItem,
        _pool: &Pool<Sqlite>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Modifying <Cakupan={}> with <{}:{}>",
            self.0,
            parent.id,
            parent.keterangan
        );
        todo!()
    }
}
