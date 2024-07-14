//! The main data structure of a dictionary app.

use crate::{
    changes::{AttachmentMod, CompareAttachable, FieldMod},
    data::KonsepItemMod,
    io::interface::{
        AttachmentItemMod, FromView, FromViewMap, IntoViewMap, Item, ItemMod, SubmitItem,
    },
    prelude::*,
};

use crate::io::interface::SubmitMod;
use std::collections::HashMap;
use tracing::instrument;

use super::konsep::KonsepHashMap;

/// A lemma is an entry of a dictionary which shows a word form and its corresponding [concepts](KonsepItem).
///
/// The structure of a lemma in json is equivalent to the following:
/// ```
/// use serde_json::json;
/// # use database::data::LemmaItem;
///
/// let lemma_in_json = json!({
///     "id": 1,
///     "lemma": "aplikasi",
///     "konseps": [
///         {
///             "id": 1,
///             "keterangan": "program komputer yang direka khusus untuk kegunaan tertentu",
///             "golongan_kata": "kata nama",
///             "cakupans": ["teknologi maklumat"],
///             "kata_asing": [
///                 {"nama": "application", "bahasa": "en"},
///             ]
///         }
///     ]
/// });
///
/// let lemma: LemmaItem = serde_json::from_value(lemma_in_json).unwrap();
/// ```
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, ts_rs::TS)]
#[ts(export, export_to = "../../src/bindings/")]
pub struct LemmaItem {
    pub id: AutoGen<i64>,
    pub lemma: String,
    pub konseps: Vec<KonsepItem>,
}

/// A modified [LemmaItem].
///
/// Given two [LemmaItems](LemmaItem) that refers to the same lemma,
/// one applies the function [`old.modify_into(&new)`](LemmaItem::modify_into())
/// to return [`LemmaItemMod`] that tracks the modifications from `old` to `new`.
///
/// ## Example
/// ```
/// use serde_json::json;
/// use database::changes::{AttachmentMod, FieldMod};
/// use database::data::{CakupanItem, KataAsingItem, KonsepItemMod, LemmaItem, LemmaItemMod};
/// use database::io::interface::Item;
/// use database::types::AutoGen;
///
/// let old = json!({
///     "id": 1,
///     "lemma": "aplikasi",
///     "konseps": [
///         {
///             "id": 1,
///             "keterangan": "program komputer yang direka khusus untuk kegunaan tertentu",
///             "golongan_kata": "kata nama",
///             "cakupans": ["teknologi maklumat"],
///             "kata_asing": [
///                 {"nama": "application", "bahasa": "en"},
///             ]
///         }
///     ]
/// });
/// let new = json!({
///     "id": 1,
///     "lemma": "aplikasi",
///     "konseps": [
///         {
///             "id": 1,
///             "keterangan": "program komputer yang direka khusus untuk kegunaan tertentu",
///             "golongan_kata": "kata nama",
///             "cakupans": ["teknologi maklumat"],
///             "kata_asing": [
///                 {"nama": "application", "bahasa": "en"},
///                 // A new `kata_asing` is added.
///                 {"nama": "アプリ", "bahasa": "jp"},
///             ]
///         },
///         // A new konsep item is attached to this lemma item which implies that the id is unknown.
///         {
///             "id": null,
///             "keterangan": "kegunaan yang boleh dipraktikkan",
///             "golongan_kata": "kata nama",
///             "cakupans": ["kemasyarakatan", "teknologi dan inovasi"],
///             // The vector can be empty if the corresponding tag is yet unknown.
///             "kata_asing": [ ]
///         }
///     ]
/// });
///
/// let lemma_old: LemmaItem = serde_json::from_value(old).unwrap();
/// let lemma_new: LemmaItem = serde_json::from_value(new).unwrap();
/// let lemma_modded: LemmaItemMod = lemma_old.modify_into(&lemma_new).unwrap();
///
/// assert_eq!(lemma_modded.lemma, FieldMod::Fixed("aplikasi".to_string()));
/// assert_eq!(lemma_modded.konseps.attached, vec![
/// KonsepItemMod {
/// id: AutoGen::Unknown,
/// keterangan: FieldMod::Fixed("kegunaan yang boleh dipraktikkan".to_string()),
/// golongan_kata: FieldMod::Fixed("kata nama".to_string()),
/// cakupans: AttachmentMod {
/// attached: vec![CakupanItem::from("kemasyarakatan"), CakupanItem::from("teknologi dan inovasi")],detached: vec![],modified: vec![],},
/// kata_asing: AttachmentMod::from(Vec::<KataAsingItem>::new())
/// }]);
/// assert_eq!(lemma_modded.konseps.modified, vec![
/// KonsepItemMod {
/// id: AutoGen::Known(1),
/// keterangan: FieldMod::Fixed("program komputer yang direka khusus untuk kegunaan tertentu".to_string()),
/// golongan_kata: FieldMod::Fixed("kata nama".to_string()),
/// cakupans: AttachmentMod {
///  attached: vec![],detached: vec![],modified: vec![],},
/// kata_asing: AttachmentMod {
///  attached: vec![KataAsingItem { nama: "アプリ".to_string(),bahasa: "jp".to_string()}],detached: vec![],modified: vec![],},}
/// ]);
/// assert_eq!(lemma_modded.konseps.detached, vec![]);
/// ```
#[derive(Debug, Clone)]
pub struct LemmaItemMod {
    pub id: AutoGen<i64>,
    pub lemma: FieldMod<String>,
    pub konseps: AttachmentMod<KonsepItemMod>,
}

impl Item for LemmaItem {
    type IntoMod = LemmaItemMod;
    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        if self.id != other.id {
            Err(BackendError {
                message: String::from("ID Assertion error"),
            })
        } else {
            Ok(LemmaItemMod {
                id: self.id,
                lemma: FieldMod::compare(self.lemma.clone(), other.lemma.clone()),
                konseps: self.compare_attachment(other.konseps.to_owned()),
            })
        }
    }

    fn partial_from_mod(other: &LemmaItemMod) -> Self {
        LemmaItem {
            id: other.id,
            lemma: other.lemma.value().to_string(),
            konseps: vec![],
        }
    }
}

impl ItemMod for LemmaItemMod {
    type FromItem = LemmaItem;

    fn from_item(value: &Self::FromItem) -> Self {
        Self {
            id: value.id,
            lemma: FieldMod::Fixed(value.lemma.clone()),
            konseps: AttachmentMod::from(value.konseps.clone()),
        }
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl SubmitMod for LemmaItemMod {
    type Engine = sqlx::Sqlite;
    #[instrument(skip_all)]
    async fn submit_mod(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        let item = LemmaItem::partial_from_mod(self);
        tracing::trace!("Submitting <{}:{}>", item.id, item.lemma);
        item.submit_partial(pool).await?;
        self.konseps.submit_changes_with(&item, pool).await?;
        Ok(())
    }
}

impl PartialEq for LemmaItem {
    fn eq(&self, other: &Self) -> bool {
        let konseps = Vec::from_iter(self.konseps.clone());
        self.lemma == other.lemma
            && other
                .konseps
                .iter()
                .filter(|a| !konseps.contains(a))
                .collect_vec()
                .is_empty()
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl SubmitItem for LemmaItem {
    type Engine = sqlx::Sqlite;
    async fn submit_full(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        let _ = self.submit_partial(pool).await?;
        for konsep in self.konseps.iter() {
            KonsepItemMod::from_item(konsep)
                .submit_attachment_to(self, pool)
                .await?;
        }
        Ok(())
    }

    async fn submit_partial(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"INSERT or IGNORE INTO lemma (id, nama) VALUES (?, ?)"#,
            self.id,
            self.lemma
        }
        .execute(pool)
        .await?;
        Ok(())
    }

    async fn submit_full_removal(&self, _pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        todo!()
    }

    async fn submit_partial_removal(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"DELETE FROM lemma WHERE (lemma.id = ? AND lemma.nama = ?)"#,
            self.id,
            self.lemma
        }
        .execute(pool)
        .await?;
        Ok(())
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl SubmitItem for LemmaItem {
    type Engine = sqlx::Postgres;

    async fn submit_full(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        let _ = self.submit_partial(pool).await?;
        for konsep in self.konseps.iter() {
            KonsepItemMod::from_item(konsep)
                .submit_attachment_to(self, pool)
                .await?;
        }
        Ok(())
    }

    async fn submit_partial(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"INSERT or IGNORE INTO lemma (id, nama) VALUES (?, ?)"#,
            self.id,
            self.lemma
        }
        .execute(pool)
        .await?;
        Ok(())
    }

    async fn submit_full_removal(&self, _pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        todo!()
    }

    async fn submit_partial_removal(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"DELETE FROM lemma WHERE (lemma.id = ? AND lemma.nama = ?)"#,
            self.id,
            self.lemma
        }
        .execute(pool)
        .await?;
        Ok(())
    }
}

impl FromViewMap for LemmaItem {
    type KEY = (i64, String);
    type VALUE = KonsepHashMap;

    fn from_viewmap(value: &HashMap<Self::KEY, Self::VALUE>) -> Vec<LemmaItem> {
        let mut data = Vec::<LemmaItem>::new();
        for (lemma, konsep_map) in value.iter() {
            data.push(LemmaItem {
                id: AutoGen::Known(lemma.0),
                lemma: lemma.1.clone(),
                konseps: KonsepItem::from_viewmap(konsep_map),
            })
        }
        data
    }
}
impl FromView for LemmaItem {
    type VIEW = LemmaWithKonsepView;

    fn from_views(views: &Vec<Self::VIEW>) -> Vec<LemmaItem> {
        Self::from_viewmap(&(views.clone().into_viewmap()))
    }
}
