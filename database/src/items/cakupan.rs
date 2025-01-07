//! Implement traits for [schema::items::cakupan::Cakupan]

use crate::engine::DbEngine;
use crate::io::interface::{AttachmentItemMod, FromView, Item, ItemMod, SubmitItem};
use crate::prelude::*;

use schema::items::cakupan::Cakupan;
use schema::items::konsep::Konsep;

use tracing::instrument;

pub(crate) type CakupanMod = Cakupan;

impl Item for Cakupan {
    type IntoMod = Cakupan;

    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        Ok(other.to_owned())
    }

    fn partial_from_mod(other: &Self::IntoMod) -> Self {
        other.to_owned()
    }
}

impl ItemMod for Cakupan {
    type FromItem = Cakupan;

    fn from_item(value: &Self::FromItem) -> Self {
        value.to_owned()
    }
}

impl FromView for Cakupan {
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

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl<I: Sync + PartialEq + Copy + Clone> AttachmentItemMod<Konsep<I>, sqlx::SqlitePool>
    for Cakupan
{
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &Konsep<I>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Attaching <Cakupan={}> to <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        sqlx::query! {
        r#"
            INSERT or IGNORE INTO cakupan (nama) VALUES (?);
            INSERT or IGNORE INTO cakupan_x_konsep (cakupan_id, konsep_id)
            VALUES (
                (SELECT id FROM cakupan WHERE cakupan.nama = ?),
                (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                );"#,
            value,
            value,
            parent.keterangan
        }
        .execute(engine.pool())
        .await
        .expect("Error attaching cakupan to konsep");
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &Konsep<I>,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Detaching <Cakupan={}> from <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        sqlx::query! {
        r#" DELETE FROM cakupan_x_konsep AS cxk
            WHERE (
                cxk.cakupan_id = (SELECT id FROM cakupan WHERE cakupan.nama = ?)
                AND
                cxk.konsep_id = (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                );"#,
            value,
            parent.keterangan
        }
        .execute(engine.pool())
        .await
        .expect("Error detaching cakupan from konsep");
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &Konsep<I>,
        _engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Modifying <Cakupan={}> with <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        todo!()
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl<I: Sync + PartialEq + Copy + Clone> AttachmentItemMod<Konsep<I>, sqlx::PgPool> for Cakupan {
    #[instrument(skip_all)]
    async fn submit_attachment_to(
        &self,
        parent: &Konsep<I>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Attaching <Cakupan={}> to <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        sqlx::query! {
            r#"INSERT INTO cakupan (nama) VALUES ($1) ON CONFLICT (nama) DO NOTHING;"#,
            value
        }
        .execute(engine.pool())
        .await
        .expect("Error attaching cakupan to konsep");

        sqlx::query! {
        r#"INSERT INTO cakupan_x_konsep (cakupan_id, konsep_id)
        VALUES (
            (SELECT id FROM cakupan WHERE cakupan.nama = $1),
            (SELECT id FROM konsep WHERE konsep.keterangan = $2)
            ) ON CONFLICT (cakupan_id, konsep_id) DO NOTHING;"#,
            value,
            parent.keterangan
        }
        .execute(engine.pool())
        .await
        .expect("Error attaching cakupan to konsep");
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &Konsep<I>,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Detaching <Cakupan={}> from <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        sqlx::query! {
        r#" DELETE FROM cakupan_x_konsep AS cxk
        WHERE (
            cxk.cakupan_id = (SELECT id FROM cakupan WHERE cakupan.nama = $1)
            AND
            cxk.konsep_id = (SELECT id FROM konsep WHERE konsep.keterangan = $2)
            );"#,
            value,
            parent.keterangan
        }
        .execute(engine.pool())
        .await
        .expect("Error detaching cakupan from konsep");
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &Konsep<I>,
        _engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<()> {
        let value = self.value();
        // tracing::trace!(
        //     "Modifying <Cakupan={}> with <{}:{}>",
        //     value,
        //     parent.id,
        //     parent.keterangan
        // );
        todo!()
    }
}
