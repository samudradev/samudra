//! A crate to handle database operations.
#![cfg_attr(
    debug_assertions,
    allow(dead_code, missing_docs, unused_imports, unused_variables)
)]

pub mod changes;
pub mod data;
pub mod engine;
pub mod errors;
pub mod io;
#[deprecated]
#[doc(hidden)]
pub mod operations;
#[deprecated]
pub mod states;
pub mod types;
pub mod views;

#[doc(hidden)]
pub mod prelude {
    // Datamodels
    pub(crate) use crate::data::items::kata_asing::KataAsingItem;
    pub(crate) use crate::data::items::konsep::KonsepItem;
    #[deprecated]
    pub(crate) use crate::views::LemmaWithKonsepView;

    // Types
    pub(crate) use crate::errors::BackendError;
    pub(crate) use crate::errors::Result;
    pub(crate) use crate::types::AutoGen;

    // Traits
    pub(crate) use itertools::Itertools;
}
