use crate::metatype::AutoGen;

use super::{cakupan::Cakupan, kata_asing::KataAsing};

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
pub struct Konsep<I: Copy + Clone + PartialEq> {
    pub id: AutoGen<I>,
    pub keterangan: String,
    pub golongan_kata: String,
    pub cakupans: Vec<Cakupan>,
    pub kata_asing: Vec<KataAsing>,
}
