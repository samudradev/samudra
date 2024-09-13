//! A module that contains definition of structs implementing [View].

use std::collections::HashMap;

use itertools::Itertools;

use crate::data::items::konsep::KonsepHashMap;
use crate::io::interface::IntoViewMap;

/// A [View](crate::io::interface::View) whose query joins konsep to its tags (cakupan, kata_asing)
///
/// Running this command:
/// ```no_run
/// # use database::views::LemmaWithKonsepView;
/// #
/// # tokio_test::block_on(async {
/// # let pool_url = ":memory:";
/// let pool = sqlx::SqlitePool::connect(pool_url).await.expect("Connection error");
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
    /// ID (Primary): [LemmaItem.id](crate::data::LemmaItem#structfield.id)
    pub l_id: i64,
    /// Data (Primary): [LemmaItem.nama](crate::data::LemmaItem#structfield.nama)
    pub lemma: String,
    /// ID (Secondary): [KonsepItem.id](crate::data::KonsepItem#structfield.id)
    pub k_id: i64,
    /// Data (Secondary): [KonsepItem.keterangan](crate::data::KonsepItem#structfield.keterangan)
    pub konsep: Option<String>,
    /// Data (Secondary): [KonsepItem.golongan_kata](crate::data::KataAsingItem#structfield.golongan_kata)
    pub golongan_kata: Option<String>,
    /// Attachment: [CakupanItem](crate::data::CakupanItem)
    pub cakupan: Option<String>,
    /// Attachment: [KataAsingItem.nama](crate::data::KataAsingItem#structfield.nama)
    pub kata_asing: Option<String>,
    /// Attachment: [KataAsingItem.bahasa](crate::data::KataAsingItem#structfield.bahasa)
    pub bahasa_asing: Option<String>,
}

#[cfg(feature = "sqlite")]
impl crate::io::interface::View for LemmaWithKonsepView {
    type SOURCE = sqlx::Sqlite;
}

#[cfg(feature = "postgres")]
impl crate::io::interface::View for LemmaWithKonsepView {
    type SOURCE = sqlx::Postgres;
}
#[cfg(all(feature = "sqlite", feature = "postgres"))]
compile_error!("The code as it is currently designed results in conflicting implementations from features `sqlite` and `postgres`. TODO: FIX");

#[cfg(any(feature = "sqlite", feature = "postgres"))]
impl LemmaWithKonsepView {
    /// Query a single lemma with its associated konseps and attachments.
    pub async fn query_lemma(
        lemma: String,
        pool: &sqlx::Pool<<Self as crate::io::interface::View>::SOURCE>,
    ) -> sqlx::Result<Vec<Self>> {
        sqlx::query_file_as!(
            Self,
            "transactions/select_lemma_with_konsep_view.sql",
            lemma
        )
        .fetch_all(pool)
        .await
    }

    /// Query all lemmas.
    pub async fn query_all(
        pool: &sqlx::Pool<<Self as crate::io::interface::View>::SOURCE>,
    ) -> sqlx::Result<Vec<Self>> {
        // TODO: Might be a good idea to add limit
        // TODO: And maybe sort by reverse chronology
        sqlx::query_file_as!(
            Self,
            "transactions/select_lemma_with_konsep_view.sql",
            None::<String>
        )
        .fetch_all(pool)
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
// #[cfg(test)]
// mod test {
//     use super::*;
//
//     #[sqlx::test(fixtures("lemma", "lemma_2"))]
//     fn test_lemma_w_konsep_view(pool: sqlx::Pool<sqlx::Sqlite>) {
//         let views: Vec<LemmaWithKonsepView> = LemmaWithKonsepView::query_all(&pool).await.unwrap();
//         let mut data = dbg!(LemmaItem::from_views(&views)
//             .into_iter()
//             .sorted_by(|a, b| a.lemma.cmp(&b.lemma)));
//         assert_eq!(
//             data.next().unwrap(),
//             LemmaItem {
//                 id: DbProvided::Known(1),
//                 lemma: "cakera tokokan".into(),
//                 konseps: vec![KonsepItem {
//                     id: DbProvided::Known(1),
//                     keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
//                     golongan_kata: "kata nama".into(),
//                     cakupans: vec!["Teori Relativiti".into(), "Astrofizik".into(),],
//                     kata_asing: vec![KataAsingItem {
//                         nama: "accretion disk".into(),
//                         bahasa: "english".into(),
//                     }],
//                 },],
//             },
//         );
//         assert_eq!(
//             data.next().unwrap(),
//             LemmaItem {
//                 id: DbProvided::Known(2),
//                 lemma: "ufuk peristiwa".into(),
//                 konseps: vec![KonsepItem {
//                     id: DbProvided::Known(2),
//                     keterangan: "sempadan terluar lohong hitam".into(),
//                     golongan_kata: "kata nama".into(),
//                     cakupans: vec!["Teori Relativiti".into(), "Astrofizik".into(),],
//                     kata_asing: vec![KataAsingItem {
//                         nama: "event horizon".into(),
//                         bahasa: "english".into(),
//                     }],
//                 },],
//             }
//         );
//     }
//
//     #[sqlx::test(fixtures("lemma", "lemma_2"))]
//     fn test_lemma_w_empty_konsep_query_view(pool: sqlx::Pool<sqlx::Sqlite>) {
//         let views: Vec<LemmaWithKonsepView> =
//             LemmaWithKonsepView::query_lemma("cakera tokokan".into(), &pool)
//                 .await
//                 .unwrap();
//         let mut data = dbg!(LemmaItem::from_views(&views)
//             .into_iter()
//             .sorted_by(|a, b| a.lemma.cmp(&b.lemma)));
//         assert_eq!(
//             data.next(),
//             Some(LemmaItem {
//                 id: DbProvided::Known(1),
//                 lemma: "cakera tokokan".into(),
//                 konseps: vec![KonsepItem {
//                     id: DbProvided::Known(1),
//                     keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
//                     golongan_kata: "kata nama".into(),
//                     cakupans: vec!["Astrofizik".into(), "Teori Relativiti".into(),],
//                     kata_asing: vec![KataAsingItem {
//                         nama: "accretion disk".into(),
//                         bahasa: "english".into(),
//                     }],
//                 },],
//             }),
//         );
//     }
//
//     #[sqlx::test(fixtures("defaults"))]
//     fn test_lemma_w_empty_kata_asing(pool: sqlx::Pool<sqlx::Sqlite>) {
//         let mut item = LemmaItem {
//             id: DbProvided::Unknown,
//             lemma: "cakera tokokan".into(),
//             konseps: vec![KonsepItem {
//                 id: DbProvided::Unknown,
//                 keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
//                 golongan_kata: "kata nama".into(),
//                 cakupans: vec!["Astrofizik".into(), "Teori Relativiti".into()],
//                 kata_asing: vec![],
//             }],
//         };
//         let _ = item.clone().insert_safe(&pool).await.unwrap();
//         let views: Vec<LemmaWithKonsepView> = LemmaWithKonsepView::query_all(&pool).await.unwrap();
//         let data = LemmaItem::from_views(&views);
//         item.id = DbProvided::Known(1);
//         let k = item.konseps.first_mut().unwrap();
//         k.id = DbProvided::Known(1);
//         assert_eq!(data.iter().next(), Some(&item),);
//     }
//     #[sqlx::test(fixtures("defaults"))]
//     fn test_lemma_w_empty_cakupan(pool: sqlx::Pool<sqlx::Sqlite>) {
//         let mut item = LemmaItem {
//             id: DbProvided::Unknown,
//             lemma: "cakera tokokan".into(),
//             konseps: vec![KonsepItem {
//                 id: DbProvided::Unknown,
//                 keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
//                 golongan_kata: "kata nama".into(),
//                 cakupans: vec![],
//                 kata_asing: vec![KataAsingItem {
//                     nama: "accretion disk".into(),
//                     bahasa: "english".into(),
//                 }],
//             }],
//         };
//         let _ = item.clone().insert_safe(&pool).await.unwrap();
//         let views: Vec<LemmaWithKonsepView> = LemmaWithKonsepView::query_all(&pool).await.unwrap();
//         let data = LemmaItem::from_views(&views);
//         item.id = DbProvided::Known(1);
//         let k = item.konseps.first_mut().unwrap();
//         k.id = DbProvided::Known(1);
//         assert_eq!(data.iter().next(), Some(&item),);
//     }
// }
