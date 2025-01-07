//! Implements traits for [schema::items::konsep::Konsep]

use std::collections::HashMap;
use std::fmt::{Debug, Display};

use crate::changes::{AttachmentMod, CompareAttachable, FieldMod};
use crate::engine::DbEngine;
use crate::io::interface::{AttachmentItemMod, FromView, FromViewMap, Item, ItemMod};
use crate::prelude::*;

use schema::items::cakupan::Cakupan;
use schema::items::kata_asing::KataAsing;
use schema::items::konsep::Konsep;
use schema::items::lemma::Lemma;
use schema::metatype::AutoGen;

use tracing::instrument;

/// A modified [Konsep].
///
/// Its usage is similar to [LemmaMod](crate::items::lemma::LemmaMod).
#[derive(Clone, PartialEq)]
pub struct KonsepMod<I> {
    pub id: AutoGen<I>,
    pub keterangan: FieldMod<String>,
    pub golongan_kata: FieldMod<String>,
    pub cakupans: AttachmentMod<Cakupan>,
    pub kata_asing: AttachmentMod<KataAsing>,
}

type Key<I> = (
    /*id*/ I,
    /*keterangan*/ Option<String>,
    /*golongan kata*/ Option<String>,
);
type Value = Vec<LemmaWithKonsepView>;
pub(crate) type KonsepHashMap<I> = HashMap<Key<I>, Value>;

impl<I: PartialEq + Copy + Clone> Item for Konsep<I> {
    type IntoMod = KonsepMod<I>;
    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        if self.id != other.id {
            return Err(BackendError {
                message: format!("ID Assertion error"),
            });
        }
        Ok(KonsepMod {
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
        Konsep {
            id: other.id,
            keterangan: other.keterangan.value().to_string(),
            golongan_kata: other.golongan_kata.value().to_string(),
            cakupans: vec![],
            kata_asing: vec![],
        }
    }
}

impl<I: Copy + Clone + PartialEq> FromViewMap for Konsep<I> {
    type KEY = Key<I>;
    type VALUE = Value;
    fn from_viewmap(value: &KonsepHashMap<I>) -> Vec<Self> {
        let mut data = Vec::new();
        for (konsep, views) in value.iter().filter(|((_, kon, _), _)| kon.is_some()) {
            data.push(Konsep {
                id: AutoGen::Known(konsep.0),
                keterangan: konsep
                    .1
                    .clone()
                    .expect("None should have been filtered out"),
                golongan_kata: konsep.2.clone().unwrap_or_default(),
                cakupans: Cakupan::from_views(views),
                kata_asing: KataAsing::from_views(views),
            })
        }
        data
    }
}

impl<I: PartialEq + Copy + Clone> ItemMod for KonsepMod<I> {
    type FromItem = Konsep<I>;

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

impl<I: Copy + Clone + PartialEq> CompareAttachable<Cakupan, Cakupan> for Konsep<I> {
    fn items(&self) -> Vec<Cakupan> {
        Vec::clone(&self.cakupans)
    }
}
impl<I: Copy + Clone + PartialEq> CompareAttachable<KataAsing, KataAsing> for Konsep<I> {
    fn items(&self) -> Vec<KataAsing> {
        Vec::clone(&self.kata_asing)
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl AttachmentItemMod<Lemma<i32>, sqlx::SqlitePool> for KonsepMod<i32> {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let konsep = Konsep::partial_from_mod(self);
        // tracing::trace!(
        // "Attaching <{}:{}> to <{}:{}>",
        // konsep.id,
        // konsep.keterangan,
        // parent.id,
        // parent.lemma
        // );
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
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        // tracing::trace!(
        // "Detaching <{}:{}> from <{}:{}>",
        // self.id,
        // self.keterangan.value(),
        // parent.id,
        // parent.lemma
        // );
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
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let konsep = Konsep::partial_from_mod(self);
        // tracing::trace!(
        // "Modifying <{}:{}> with <{}:{}>",
        // konsep.id,
        // konsep.keterangan,
        // parent.id,
        // parent.lemma
        // );
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
impl AttachmentItemMod<Lemma<i32>, sqlx::PgPool> for KonsepMod<i32> {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let konsep = Konsep::partial_from_mod(self);
        // tracing::trace!(
        // "Attaching <{}:{}> to <{}:{}>",
        // konsep.id,
        // konsep.keterangan,
        // parent.id,
        // parent.lemma
        // );
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
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        // tracing::trace!(
        // "Detaching <{}:{}> from <{}:{}>",
        // self.id,
        // self.keterangan.value(),
        // parent.id,
        // parent.lemma
        // );
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
        parent: &Lemma<i32>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let konsep = Konsep::partial_from_mod(self);
        // tracing::trace!(
        //     "Modifying <{}:{}> with <{}:{}>",
        //     konsep.id,
        //     konsep.keterangan,
        //     parent.id,
        //     parent.lemma
        // );
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
