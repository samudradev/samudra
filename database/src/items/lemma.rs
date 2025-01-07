//! Implements traits for [schema::items::lemma::Lemma]

use crate::{
    changes::{AttachmentMod, CompareAttachable, FieldMod},
    io::interface::{
        AttachmentItemMod, FromView, FromViewMap, IntoViewMap, Item, ItemMod, SubmitItem,
    },
    prelude::*,
};

use std::collections::HashMap;

use crate::engine::DbEngine;
use crate::io::interface::SubmitMod;
use crate::items::konsep::{KonsepHashMap, KonsepMod};

use schema::items::konsep::Konsep;
use schema::items::lemma::Lemma;
use schema::metatype::AutoGen;

use tracing::instrument;

/// A modified [Lemma].
///
/// Given two [Lemmas](Lemma) that refers to the same lemma,
/// one applies the function [`old.modify_into(&new)`](Lemma::modify_into())
/// to return [`LemmaMod`] that tracks the modifications from `old` to `new`.
///
/// ## Example
/// ```no_run
/// use serde_json::json;
///
/// use database::changes::{AttachmentMod, FieldMod};
/// use database::items::{konsep::KonsepMod, lemma::LemmaMod};
/// use database::io::interface::Item;
///
/// use schema::items::lemma::Lemma;
/// use schema::items::konsep::Konsep;
/// use schema::items::kata_asing::KataAsing;
/// use schema::items::cakupan::Cakupan;
/// use schema::metatype::AutoGen;
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
/// let lemma_old: Lemma<i64> = serde_json::from_value(old).unwrap();
/// let lemma_new: Lemma<i64> = serde_json::from_value(new).unwrap();
/// let lemma_modded: LemmaMod<i64> = lemma_old.modify_into(&lemma_new).unwrap();
///
/// assert!(lemma_modded.lemma == FieldMod::Fixed("aplikasi".to_string()));
/// assert!(lemma_modded.konseps.attached == vec![
/// KonsepMod {
/// id: AutoGen::Unknown,
/// keterangan: FieldMod::Fixed("kegunaan yang boleh dipraktikkan".to_string()),
/// golongan_kata: FieldMod::Fixed("kata nama".to_string()),
/// cakupans: AttachmentMod {
/// attached: vec![Cakupan::from("kemasyarakatan"), Cakupan::from("teknologi dan inovasi")],detached: vec![],modified: vec![],},
/// kata_asing: AttachmentMod::from(Vec::<KataAsing>::new())
/// }]);
/// assert!(lemma_modded.konseps.modified == vec![
/// KonsepMod {
/// id: AutoGen::Known(1),
/// keterangan: FieldMod::Fixed("program komputer yang direka khusus untuk kegunaan tertentu".to_string()),
/// golongan_kata: FieldMod::Fixed("kata nama".to_string()),
/// cakupans: AttachmentMod {
///  attached: vec![],detached: vec![],modified: vec![],},
/// kata_asing: AttachmentMod {
///  attached: vec![KataAsing { nama: "アプリ".to_string(),bahasa: "jp".to_string()}],detached: vec![],modified: vec![],},}
/// ]);
/// assert!(lemma_modded.konseps.detached == vec![]);
/// ```
#[derive(Clone)]
pub struct LemmaMod<I: PartialEq + Copy + Clone> {
    pub id: AutoGen<I>,
    pub lemma: FieldMod<String>,
    pub konseps: AttachmentMod<KonsepMod<I>>,
}

impl<I: PartialEq + Copy + Clone> Item for Lemma<I> {
    type IntoMod = LemmaMod<I>;
    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        if self.id != other.id {
            Err(BackendError {
                message: String::from("ID Assertion error"),
            })
        } else {
            Ok(LemmaMod {
                id: self.id,
                lemma: FieldMod::compare(self.lemma.clone(), other.lemma.clone()),
                konseps: self.compare_attachment(other.konseps.to_owned()),
            })
        }
    }

    fn partial_from_mod(other: &LemmaMod<I>) -> Self {
        Lemma {
            id: other.id,
            lemma: other.lemma.value().to_string(),
            konseps: vec![],
        }
    }
}

impl<I: PartialEq + Copy + Clone> ItemMod for LemmaMod<I> {
    type FromItem = Lemma<I>;

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
impl SubmitMod<sqlx::SqlitePool> for LemmaMod<i32> {
    #[instrument(skip_all)]
    async fn submit_mod(&self, engine: &DbEngine<sqlx::SqlitePool>) -> sqlx::Result<()> {
        let item = Lemma::partial_from_mod(self);
        // tracing::trace!("Submitting <{}:{}>", item.id, item.lemma);
        item.submit_partial(engine).await?;
        self.konseps.submit_changes_with(&item, engine).await?;
        Ok(())
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl SubmitItem<sqlx::SqlitePool> for Lemma<i32> {
    async fn submit_full(&self, engine: &DbEngine<sqlx::SqlitePool>) -> sqlx::Result<()> {
        let _ = self.submit_partial(engine).await?;
        for konsep in self.konseps.iter() {
            KonsepMod::from_item(konsep)
                .submit_attachment_to(self, engine)
                .await?;
        }
        Ok(())
    }

    async fn submit_partial(&self, engine: &DbEngine<sqlx::SqlitePool>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"INSERT or IGNORE INTO lemma (id, nama) VALUES (?, ?)"#,
            self.id,
            self.lemma
        }
        .execute(engine.pool())
        .await?;
        Ok(())
    }

    async fn submit_full_removal(&self, _engine: &DbEngine<sqlx::SqlitePool>) -> sqlx::Result<()> {
        todo!()
    }

    async fn submit_partial_removal(
        &self,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        sqlx::query! {
            r#"DELETE FROM lemma WHERE (lemma.id = ? AND lemma.nama = ?)"#,
            self.id,
            self.lemma
        }
        .execute(engine.pool())
        .await?;
        Ok(())
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl SubmitItem<sqlx::PgPool> for Lemma<i32> {
    async fn submit_full(&self, engine: &DbEngine<sqlx::PgPool>) -> sqlx::Result<()> {
        let _ = self.submit_partial(engine).await?;
        for konsep in self.konseps.iter() {
            KonsepMod::from_item(konsep)
                .submit_attachment_to(self, engine)
                .await?;
        }
        Ok(())
    }

    async fn submit_partial(&self, engine: &DbEngine<sqlx::PgPool>) -> sqlx::Result<()> {
        match self.id {
            AutoGen::Known(i) => sqlx::query! {
                r#"INSERT INTO lemma (id, nama) VALUES ($1, $2);"#,
                i,
                self.lemma
            },
            AutoGen::Unknown => sqlx::query! {
                r#"INSERT INTO lemma (nama) VALUES ($1);"#,
                self.lemma
            },
        }
        .execute(engine.pool())
        .await?;
        Ok(())
    }

    async fn submit_full_removal(&self, _engine: &DbEngine<sqlx::PgPool>) -> sqlx::Result<()> {
        todo!()
    }

    async fn submit_partial_removal(&self, engine: &DbEngine<sqlx::PgPool>) -> sqlx::Result<()> {
        match self.id {
            AutoGen::Known(i) => {
                sqlx::query! {
                    r#"DELETE FROM lemma WHERE (lemma.id = $1 AND lemma.nama = $2)"#,
                    i,
                    self.lemma
                }
                .execute(engine.pool())
                .await?
            }
            AutoGen::Unknown => todo!(),
        };
        Ok(())
    }
}

impl FromViewMap for Lemma<i64> {
    type KEY = (i64, String);
    type VALUE = KonsepHashMap<i64>;

    fn from_viewmap(value: &HashMap<Self::KEY, Self::VALUE>) -> Vec<Lemma<i64>> {
        let mut data = Vec::<Lemma<i64>>::new();
        for (lemma, konsep_map) in value.iter() {
            data.push(Lemma {
                id: AutoGen::Known(lemma.0),
                lemma: lemma.1.clone(),
                konseps: Konsep::from_viewmap(konsep_map),
            })
        }
        data
    }
}
impl FromViewMap for Lemma<i32> {
    type KEY = (i32, String);
    type VALUE = KonsepHashMap<i32>;

    fn from_viewmap(value: &HashMap<Self::KEY, Self::VALUE>) -> Vec<Lemma<i32>> {
        let mut data = Vec::<Lemma<i32>>::new();
        for (lemma, konsep_map) in value.iter() {
            data.push(Lemma {
                id: AutoGen::Known(lemma.0),
                lemma: lemma.1.clone(),
                konseps: Konsep::from_viewmap(konsep_map),
            })
        }
        data
    }
}

impl FromView for Lemma<i64> {
    type VIEW = LemmaWithKonsepView;

    fn from_views(views: &Vec<Self::VIEW>) -> Vec<Lemma<i64>> {
        Self::from_viewmap(&(views.clone().into_viewmap()))
    }
}
