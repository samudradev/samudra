//! Contains struct [KataAsingItem] which map a foreign word with its language of origin.

use std::fmt::Display;

use crate::io::interface::{AttachmentItemMod, FromView, Item, ItemMod, SubmitItem};
use crate::prelude::*;

/// Contains a foreign word with its language of origin.
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize, PartialEq, ts_rs::TS)]
#[ts(export, export_to = "../../src/bindings/")]
pub struct KataAsingItem {
    pub nama: String,
    pub bahasa: String,
}

impl ItemMod for KataAsingItem {
    type FromItem = KataAsingItem;

    fn from_item(value: &Self::FromItem) -> Self {
        value.clone()
    }
}

impl KataAsingItem {
    pub fn null() -> Self {
        KataAsingItem {
            nama: "".into(),
            bahasa: "".into(),
        }
    }
}

impl Item for KataAsingItem {
    type IntoMod = KataAsingItem;

    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod> {
        Ok(other.clone())
    }

    fn partial_from_mod(other: &Self::IntoMod) -> Self {
        other.clone()
    }
}

impl FromView for KataAsingItem {
    type VIEW = LemmaWithKonsepView;

    fn from_views(value: &Vec<Self::VIEW>) -> Vec<Self> {
        value
            .clone()
            .into_iter()
            .filter(|a| a.kata_asing.is_some())
            .into_group_map_by(|a| {
                (
                    a.kata_asing
                        .clone()
                        .expect("None should have been filtered out"),
                    a.bahasa_asing
                        .clone()
                        .expect("None should have been filtered out"),
                )
            })
            .keys()
            .map(|(nama, bahasa)| KataAsingItem {
                nama: nama.into(),
                bahasa: bahasa.into(),
            })
            .collect_vec()
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl SubmitItem for KataAsingItem {
    type Engine = sqlx::Sqlite;
    async fn submit_full(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        sqlx::query! {
            r#"INSERT or IGNORE INTO kata_asing (nama, bahasa) VALUES (?,?)"#,
            self.nama,
            self.bahasa
        }
        .execute(pool)
        .await?;
        Ok(())
    }

    async fn submit_partial(&self, pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        self.submit_full(pool).await
    }

    async fn submit_full_removal(&self, _pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        todo!()
    }

    async fn submit_partial_removal(&self, _pool: &sqlx::Pool<Self::Engine>) -> sqlx::Result<()> {
        todo!()
    }
}

#[cfg(feature = "sqlite")]
#[async_trait::async_trait]
impl<I: Display + Sync + PartialEq + Copy + Clone> AttachmentItemMod<KonsepItem<I>>
    for KataAsingItem
{
    type Engine = sqlx::Sqlite;

    async fn submit_attachment_to(
        &self,
        parent: &KonsepItem<I>,
        pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Attaching <KataAsing {}:{}> to <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
             r#"INSERT or IGNORE INTO kata_asing (nama, bahasa) VALUES (?,?);
                INSERT or IGNORE INTO kata_asing_x_konsep (kata_asing_id, konsep_id)
                VALUES (
                    (SELECT id FROM kata_asing WHERE kata_asing.nama = ? AND kata_asing.bahasa = ?),
                    (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                );"#,
             self.nama,
            self.bahasa,
            self.nama,
            self.bahasa,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error attaching kata_asing to konsep");
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &KonsepItem<I>,
        pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Detaching <KataAsing {}:{}> from <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
            r#"DELETE FROM kata_asing_x_konsep AS kaxk
               WHERE (
                    kaxk.kata_asing_id = (SELECT id FROM kata_asing WHERE kata_asing.nama = ? AND kata_asing.bahasa = ?)
                        AND
                    kaxk.konsep_id = (SELECT id FROM konsep WHERE konsep.keterangan = ?)
                );"#,
            self.nama,
            self.bahasa,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error detaching cakupan from konsep");
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &KonsepItem<I>,
        _pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Modifying <KataAsing {}:{}> with <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        todo!()
    }
}

#[cfg(feature = "postgres")]
#[async_trait::async_trait]
impl<I: Display + Sync + PartialEq + Copy + Clone> AttachmentItemMod<KonsepItem<I>>
    for KataAsingItem
{
    type Engine = sqlx::Postgres;

    async fn submit_attachment_to(
        &self,
        parent: &KonsepItem<I>,
        pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Attaching <KataAsing {}:{}> to <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
            r#"INSERT INTO kata_asing (nama, bahasa) VALUES ($1,$2) ON CONFLICT (nama, bahasa) DO NOTHING;"#, self.nama, self.bahasa
        }.execute(pool).await.expect("Error attaching kata_asing to konsep");
        sqlx::query! {
            r#"INSERT INTO kata_asing_x_konsep (kata_asing_id, konsep_id)
                VALUES (
                    (SELECT id FROM kata_asing WHERE kata_asing.nama = $1 AND kata_asing.bahasa = $2),
                    (SELECT id FROM konsep WHERE konsep.keterangan = $3)
                ) ON CONFLICT (kata_asing_id, konsep_id) DO NOTHING;"#,
            self.nama,
            self.bahasa,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error attaching kata_asing to konsep");
        Ok(())
    }
    async fn submit_detachment_from(
        &self,
        parent: &KonsepItem<I>,
        pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Detaching <KataAsing {}:{}> from <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        sqlx::query! {
            r#"DELETE FROM kata_asing_x_konsep AS kaxk
               WHERE (
                    kaxk.kata_asing_id = (SELECT id FROM kata_asing WHERE kata_asing.nama = $1 AND kata_asing.bahasa = $2)
                        AND
                    kaxk.konsep_id = (SELECT id FROM konsep WHERE konsep.keterangan = $3)
                );"#,
            self.nama,
            self.bahasa,
            parent.keterangan
        }
        .execute(pool)
        .await
        .expect("Error detaching cakupan from konsep");
        Ok(())
    }

    async fn submit_modification_with(
        &self,
        parent: &KonsepItem<I>,
        _pool: &sqlx::Pool<Self::Engine>,
    ) -> sqlx::Result<()> {
        tracing::trace!(
            "Modifying <KataAsing {}:{}> with <{}:{}>",
            self.bahasa,
            self.nama,
            parent.id,
            parent.keterangan
        );
        todo!()
    }
}
