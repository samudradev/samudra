use crate::metatype::AutoGen;

use super::konsep::Konsep;
use itertools::Itertools;

/// A lemma is an entry of a dictionary which shows a word form and its corresponding [concepts](Konsep).
///
/// The structure of a lemma in json is equivalent to the following:
/// ```
/// use serde_json::json;
/// # use schema::items::lemma::Lemma;
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
/// let lemma: Lemma<i64> = serde_json::from_value(lemma_in_json).unwrap();
/// ```
#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct Lemma<I: Copy + Clone + PartialEq> {
    pub id: AutoGen<I>,
    pub lemma: String,
    pub konseps: Vec<Konsep<I>>,
}

impl<I: PartialEq + Copy + Clone> PartialEq for Lemma<I> {
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
