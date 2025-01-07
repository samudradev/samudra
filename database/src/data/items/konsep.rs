//! The data structure of a definition is represented using [KonsepItem].

use crate::changes::{AttachmentMod, CompareAttachable, FieldMod};
use crate::engine::DbEngine;
use crate::io::interface::{AttachmentItemMod, FromView, FromViewMap, Item, ItemMod};
use crate::prelude::*;
use std::collections::HashMap;
use std::fmt::{Debug, Display};
use tracing::instrument;

use crate::data::items::cakupan::CakupanItem;
use crate::data::items::lemma::LemmaItem;

/// Represents the definition of a [LemmaItem] with tags.
///
/// A single [LemmaItem] can contain multiple [KonsepItems](KonsepItem).
/// Therefore, a map from [LemmaItem] to [KonsepItem] is a One-to-Many map.
///
/// ## Tags
/// A tag enriches a definition by presenting additional contexts to understand the meaning.
/// The following are the tags implemented in this struct:
/// - [cakupans](KonsepItem#structfield.cakupans): the communication contexts of the definition.
/// - [kata_asing](KonsepItem#structfield.kata_asing): words with equivalent meaning in other languages.
#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct KonsepItem<I> {
    pub id: AutoGen<I>,
    pub keterangan: String,
    pub golongan_kata: String,
    pub cakupans: Vec<CakupanItem>,
    pub kata_asing: Vec<KataAsingItem>,
}

impl<I: Debug> Debug for KonsepItem<I> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("KonsepItem")
            .field("id", &self.id)
            .field("keterangan", &self.keterangan)
            .field("golongan_kata", &self.golongan_kata)
            .field("cakupans", &self.cakupans)
            .field("kata_asing", &self.kata_asing)
            .finish()
    }
}

/// A modified [KonsepItem].
///
/// Its usage is similar to [LemmaItemMod](crate::data::LemmaItemMod).
#[derive(Clone, PartialEq)]
pub struct KonsepItemMod<I> {
    pub id: AutoGen<I>,
    pub keterangan: FieldMod<String>,
    pub golongan_kata: FieldMod<String>,
    pub cakupans: AttachmentMod<CakupanItem>,
    pub kata_asing: AttachmentMod<KataAsingItem>,
}

impl<I: Debug> Debug for KonsepItemMod<I> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("KonsepItemMod")
            .field("id", &self.id)
            .field("keterangan", &self.keterangan)
            .field("golongan_kata", &self.golongan_kata)
            .field("cakupans", &self.cakupans)
            .field("kata_asing", &self.kata_asing)
            .finish()
    }
}

impl<I: PartialEq + Copy + Clone> ItemMod for KonsepItemMod<I> {
    type FromItem = KonsepItem<I>;

    fn from_item(value: &Self::FromItem) -> Self {
        Self {
            id: value.id,
            keterangan: FieldMod::Fixed(value.keterangan.clone()),
            golongan_kata: FieldMod::Fixed(value.golongan_kata.clone()),
            cakupans: AttachmentMod::from(value.cakupans.clone()),
            kata_asing: AttachmentMod::from(value.kata_asing.clone()),
        }
    }
}
impl<I> KonsepItem<I> {
    pub fn null() -> Self {
        Self {
            id: AutoGen::<I>::Unknown,
            keterangan: "".into(),
            golongan_kata: "".into(),
            cakupans: vec![],
            kata_asing: vec![],
        }
    }
}

impl<I> PartialEq for KonsepItem<I> {
    fn eq(&self, other: &Self) -> bool {
        self.keterangan == other.keterangan
            && self.golongan_kata == other.golongan_kata
            // Necessary to ignore vector order
            && other
                .cakupans
                .iter()
                .filter(|&a| !self.cakupans.contains(a))
                .collect_vec()
                .is_empty()
            && other
                .kata_asing
                .iter()
                .filter(|&a| !self.kata_asing.contains(a))
                .collect_vec()
                .is_empty()
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl AttachmentItemMod<LemmaItem<i32>, sqlx::SqlitePool> for KonsepItemMod<i32> {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let konsep = KonsepItem::partial_from_mod(self);
        tracing::trace!(
            "Attaching <{}:{}> to <{}:{}>",
            konsep.id,
            konsep.keterangan,
            parent.id,
            parent.lemma
        );
        sqlx::query! {
            r#" INSERT or IGNORE INTO konsep (keterangan, lemma_id, golongan_id)
                VALUES (
                    ?,
                    (SELECT id FROM lemma WHERE lemma.nama = ?),
                    (SELECT id FROM golongan_kata WHERE golongan_kata.nama = ?)
                )
                "#,
                konsep.keterangan,
                parent.lemma,
                konsep.golongan_kata
        }
        .execute(engine.pool())
        .await?;
        self.cakupans.submit_changes_with(&konsep, engine).await?;
        self.kata_asing.submit_changes_with(&konsep, engine).await?;
        Ok(())
    }

    async fn submit_detachment_from(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Detaching <{}:{}> from <{}:{}>",
            self.id,
            self.keterangan.value(),
            parent.id,
            parent.lemma
        );
        sqlx::query! {
            r#" DELETE FROM konsep WHERE (id = ? AND lemma_id = ?)"#,
            self.id,
            parent.id
        }
        .execute(engine.pool())
        .await?;
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let konsep = KonsepItem::partial_from_mod(self);
        tracing::trace!(
            "Modifying <{}:{}> with <{}:{}>",
            konsep.id,
            konsep.keterangan,
            parent.id,
            parent.lemma
        );
        sqlx::query! {
            r#" UPDATE konsep
                SET keterangan = ?, golongan_id = (SELECT id FROM golongan_kata WHERE golongan_kata.nama = ?)
                WHERE (
                    id = ?
                    AND
                    lemma_id = ?
                )
                "#,
                konsep.keterangan,
                konsep.golongan_kata,
                konsep.id,
                parent.id,
        }
        .execute(engine.pool())
        .await?;
        self.cakupans.submit_changes_with(&konsep, engine).await?;
        self.kata_asing.submit_changes_with(&konsep, engine).await?;
        Ok(())
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl AttachmentItemMod<LemmaItem<i32>, sqlx::PgPool> for KonsepItemMod<i32> {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let konsep = KonsepItem::partial_from_mod(self);
        tracing::trace!(
            "Attaching <{}:{}> to <{}:{}>",
            konsep.id,
            konsep.keterangan,
            parent.id,
            parent.lemma
        );
        sqlx::query! {
            r#" INSERT INTO konsep (keterangan, lemma_id, golongan_id)
                VALUES (
                    $1,
                    (SELECT id FROM lemma WHERE lemma.nama = $2),
                    (SELECT id FROM golongan_kata WHERE golongan_kata.nama = $3)
                ) ON CONFLICT (id) DO NOTHING
                "#,
                konsep.keterangan,
                parent.lemma,
                konsep.golongan_kata
        }
        .execute(engine.pool())
        .await?;
        self.cakupans.submit_changes_with(&konsep, engine).await?;
        self.kata_asing.submit_changes_with(&konsep, engine).await?;
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Detaching <{}:{}> from <{}:{}>",
            self.id,
            self.keterangan.value(),
            parent.id,
            parent.lemma
        );
        match (self.id, parent.id) {
            (AutoGen::Known(i), AutoGen::Known(p)) => {
                sqlx::query! {
                    r#" DELETE FROM konsep WHERE (id = $1 AND lemma_id = $2)"#,
                    i,
                    p
                }
                .execute(engine.pool())
                .await?
            }
            (_, _) => todo!(),
        };
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &LemmaItem<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let konsep = KonsepItem::partial_from_mod(self);
        tracing::trace!(
            "Modifying <{}:{}> with <{}:{}>",
            konsep.id,
            konsep.keterangan,
            parent.id,
            parent.lemma
        );
        match (konsep.id, parent.id) {
            (AutoGen::Known(i), AutoGen::Known(p)) => sqlx::query! {
                r#" UPDATE konsep
                    SET keterangan = $1, golongan_id = (SELECT id FROM golongan_kata WHERE golongan_kata.nama = $2)
                    WHERE (
                        id = $3
                        AND
                        lemma_id = $4
                    )
                    "#,
                    konsep.keterangan,
                    konsep.golongan_kata,
                    i,
                    p,
            }
            .execute(engine.pool())
            .await?,
            (_,_) => todo!()
        };
        self.cakupans.submit_changes_with(&konsep, engine).await?;
        self.kata_asing.submit_changes_with(&konsep, engine).await?;
        Ok(())
    }
}

type Key<I> = (I, Option<String>, Option<String>);
type Value = Vec<LemmaWithKonsepView>;
pub(crate) type KonsepHashMap<I> = HashMap<Key<I>, Value>;

impl<I: PartialEq + Copy + Clone> Item for KonsepItem<I> {
    type IntoMod = KonsepItemMod<I>;
    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        if self.id != other.id {
            return Err(BackendError {
                // message: format!("ID Assertion error, {} != {}", self.id, other.id),
                message: format!("ID Assertion error"),
            });
        }
        Ok(KonsepItemMod {
            id: self.id,
            keterangan: FieldMod::compare(self.keterangan.clone(), other.keterangan.clone()),
            golongan_kata: FieldMod::compare(
                self.golongan_kata.clone(),
                other.golongan_kata.clone(),
            ),
            cakupans: self.compare_attachment(other.cakupans.clone()),
            kata_asing: self.compare_attachment(other.kata_asing.clone()),
        })
    }

    fn partial_from_mod(other: &Self::IntoMod) -> Self {
        KonsepItem {
            id: other.id,
            keterangan: other.keterangan.value().to_string(),
            golongan_kata: other.golongan_kata.value().to_string(),
            cakupans: vec![],
            kata_asing: vec![],
        }
    }
}

impl<I: Copy> FromViewMap for KonsepItem<I> {
    type KEY = Key<I>;
    type VALUE = Value;
    fn from_viewmap(value: &KonsepHashMap<I>) -> Vec<Self> {
        let mut data = Vec::new();
        for (konsep, views) in value.iter().filter(|((_, kon, _), _)| kon.is_some()) {
            data.push(KonsepItem {
                id: AutoGen::Known(konsep.0),
                keterangan: konsep
                    .1
                    .clone()
                    .expect("None should have been filtered out"),
                golongan_kata: konsep.2.clone().unwrap_or_default(),
                cakupans: CakupanItem::from_views(views),
                kata_asing: KataAsingItem::from_views(views),
            })
        }
        data
    }
}
