//! A crate to handle database operations.
#![cfg_attr(
    debug_assertions,
    allow(dead_code, missing_docs, unused_imports, unused_variables)
)]

pub mod changes;
pub mod engine;
pub mod errors;
pub mod io;
pub mod items;
#[deprecated]
pub mod states;
pub mod views;

#[doc(hidden)]
pub mod prelude {
    // Datamodels
    #[deprecated]
    pub(crate) use crate::views::LemmaWithKonsepView;

    // Types
    pub(crate) use crate::errors::BackendError;
    pub(crate) use crate::errors::Result;

    // Traits
    pub(crate) use itertools::Itertools;
}
