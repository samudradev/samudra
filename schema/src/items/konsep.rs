use super::{cakupan::Cakupan, kata_asing::KataAsing};
use crate::metatype::AutoGen;
use itertools::Itertools;

/// Represents the definition of a [Lemma](crate::items::lemma::Lemma) with tags.
///
/// A single [Lemma](crate::items::lemma::Lemma) can contain multiple [Konseps](Konsep).
/// Therefore, a map from [Lemma](crate::items::lemma::Lemma) to [Konsep] is a One-to-Many map.
///
/// ## Tags
/// A tag enriches a definition by presenting additional contexts to understand the meaning.
/// The following are the tags implemented in this struct:
/// - [cakupans](Konsep#structfield.cakupans): the communication contexts of the definition.
/// - [kata_asing](Konsep#structfield.kata_asing): words with equivalent meaning in other languages.
#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct Konsep<I: Copy + Clone + PartialEq> {
    pub id: AutoGen<I>,
    pub keterangan: String,
    pub golongan_kata: String,
    pub cakupans: Vec<Cakupan>,
    pub kata_asing: Vec<KataAsing>,
}

impl<I: Copy + Clone + PartialEq> Konsep<I> {
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

impl<I: Copy + Clone + PartialEq> PartialEq for Konsep<I> {
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
