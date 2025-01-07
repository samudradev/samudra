//! A module that contains definition of structs implementing [View].

use std::collections::HashMap;

use crate::engine::{DbEngine, LemmaWithKonsepViewOption, Query, SqlxPool};
use crate::io::interface::{IntoViewMap, View};
use crate::items::konsep::KonsepHashMap;

use itertools::Itertools;

/// A [View] whose query joins konsep to its tags (cakupan, kata_asing)
///
/// Running this command:
/// ```no_run
/// use database::views::LemmaWithKonsepView;
/// use database::engine::DbEngine;
/// #
/// # tokio_test::block_on(async {
/// # let pool_url = ":memory:";
/// let pool = DbEngine::sqlite(pool_url).await;
/// let lemma_views: Vec<LemmaWithKonsepView> = LemmaWithKonsepView::query_lemma(
///         "aplikasi".to_string(),
///          &pool
///     ).await.expect("Query error");
/// # });
/// ```
/// will bind "lemma_1" to following query and calls it:
///```sql
#[doc = include_str!("../transactions/select_lemma_with_konsep_view.sql")]
///```
#[derive(Debug, Clone, sqlx::FromRow, Default)]
pub struct LemmaWithKonsepView {
    /// ID (Primary): [Lemma.id](schema::items::lemma::Lemma#structfield.id)
    pub l_id: i64,
    /// Data (Primary): [Lemma.nama](schema::items::lemma::Lemma#structfield.nama)
    pub lemma: String,
    /// ID (Secondary): [Konsep.id](schema::items::konsep::Konsep#structfield.id)
    pub k_id: i64,
    /// Data (Secondary): [Konsep.keterangan](schema::items::konsep::Konsep#structfield.keterangan)
    pub konsep: Option<String>,
    /// Data (Secondary): [Konsep.golongan_kata](schema::items::kata_asing::KataAsing#structfield.golongan_kata)
    pub golongan_kata: Option<String>,
    /// Attachment: [CakupanItem](schema::items::cakupan::Cakupan)
    pub cakupan: Option<String>,
    /// Attachment: [KataAsing.nama](schema::items::kata_asing::KataAsing#structfield.nama)
    pub kata_asing: Option<String>,
    /// Attachment: [KataAsing.bahasa](schema::items::kata_asing::KataAsing#structfield.bahasa)
    pub bahasa_asing: Option<String>,
}

impl View for LemmaWithKonsepView {
    type SOURCE = ();
}

#[cfg(feature = "sqlite")]
impl LemmaWithKonsepView {
    /// Query a single lemma with its associated konseps and attachments.
    pub async fn query_lemma(
        lemma: String,
        engine: &DbEngine<sqlx::SqlitePool>,
    ) -> sqlx::Result<Vec<Self>> {
        engine
            .select(LemmaWithKonsepViewOption { lemma: Some(lemma) })
            .await
    }

    /// Query all lemmas.
    pub async fn query_all(engine: &DbEngine<sqlx::SqlitePool>) -> sqlx::Result<Vec<Self>> {
        // TODO: Might be a good idea to add limit
        // TODO: And maybe sort by reverse chronology
        engine
            .select(LemmaWithKonsepViewOption { lemma: None })
            .await
    }
}
#[cfg(feature = "postgres")]
impl LemmaWithKonsepView {
    /// Query a single lemma with its associated konseps and attachments.
    pub async fn query_lemma(
        lemma: String,
        engine: &DbEngine<sqlx::PgPool>,
    ) -> sqlx::Result<Vec<Self>> {
        engine
            .select(LemmaWithKonsepViewOption { lemma: Some(lemma) })
            .await
    }

    /// Query all lemmas.
    pub async fn query_all(engine: &DbEngine<sqlx::PgPool>) -> sqlx::Result<Vec<Self>> {
        // TODO: Might be a good idea to add limit
        // TODO: And maybe sort by reverse chronology
        engine
            .select(LemmaWithKonsepViewOption { lemma: None })
            .await
    }
}

impl IntoViewMap<LemmaWithKonsepView> for Vec<LemmaWithKonsepView> {
    type KEY = (i64, String);
    type VALUE = KonsepHashMap<i64>;

    fn into_viewmap(self) -> HashMap<Self::KEY, Self::VALUE> {
        self.into_iter()
            .into_group_map_by(|a| (a.l_id, a.lemma.clone()))
            .into_iter()
            .map(|(k, v): ((i64, String), Vec<LemmaWithKonsepView>)| {
                (
                    k,
                    v.into_iter()
                        .into_group_map_by(|a| (a.k_id, a.konsep.clone(), a.golongan_kata.clone())),
                )
            })
            .collect()
    }
}
