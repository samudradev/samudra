//! A module that defines interfaces

use crate::engine::{DbEngine, SqlxPool};
use crate::errors::BackendError;
use std::collections::HashMap;

/// A flat representation of data useful for reading tabular formats.
///
/// - For SQL formats, a view queries a portion of table with predefined joins and selects.
///
/// It is often used in its vector form, as it is converted into nested structs which implements [Item].
pub trait View {
    #[deprecated]
    type SOURCE;
}

/// A trait to convert Vec<[View]> into Vec<[Item]>
pub trait FromView: Sized {
    /// The view that is to be converted
    type VIEW;

    /// Converts a vector of [View] into Vec<[Item]> with no [HashMap] intermediary.
    fn from_views(views: &Vec<Self::VIEW>) -> Vec<Self>;
}

/// A trait that converts [HashMap] into Vec<[Item]>.
pub trait FromViewMap: Sized {
    /// Keys of the input [HashMap], typically the ID but can also be a tuple of identifiers.
    type KEY;
    /// The value of the input [HashMap].
    type VALUE;

    /// Converts a vector of [HashMap] into Vec<[Item]>
    fn from_viewmap(value: &HashMap<Self::KEY, Self::VALUE>) -> Vec<Self>;
}

/// A trait that converts Vec<[View]> into its intermediary form: [HashMap].
pub trait IntoViewMap<V>: IntoIterator<Item = V> {
    /// Keys of the resulting [HashMap], typically the ID.
    type KEY;
    /// The value of the resulting [HashMap].
    type VALUE;

    /// Converts an vector of [View]s to [HashMap].
    fn into_viewmap(self) -> HashMap<Self::KEY, Self::VALUE>;
}

/// A trait that follows the intended structure of its underlying data.
///
/// This is not an ORM model struct.
/// It does not intend to map with SQL table.
/// This decision choice avoids the Object-Table Impedance Mismatch.
///
/// A [View] handles the querying from SQL which contains flat tabular data.
/// While an [Item] represents the intended data which is often nested.
/// Traits like [FromView] and [FromViewMap] provides the translation layer between [View] and [Item].
pub trait Item {
    /// The Modified version of [Self].
    type IntoMod: ItemMod;

    /// Compares with other and returns the resulting modification as [Self::IntoMod].
    fn modify_into(&self, other: &Self) -> Result<Self::IntoMod, BackendError>;

    /// Instantiates a new struct with no attachment with data from [Self::IntoMod].
    ///
    /// [crate::changes::AttachmentMod] does not provide enough data to rebuild a complete vector of children,
    /// therefore, any field with [crate::changes::AttachmentMod] is ignored.

    fn partial_from_mod(other: &Self::IntoMod) -> Self;
}

/// A trait which allows item data to be submitted into SQL databases.
#[async_trait::async_trait]
pub trait SubmitItem<P: SqlxPool> {
    /// Inserts item with corresponding children.
    async fn submit_full(&self, engine: &DbEngine<P>) -> sqlx::Result<()>;

    /// Inserts item with no children.
    async fn submit_partial(&self, engine: &DbEngine<P>) -> sqlx::Result<()>;

    /// Deletes item with corresponding children.
    async fn submit_full_removal(&self, engine: &DbEngine<P>) -> sqlx::Result<()>;

    /// Deletes item with no children affected.
    async fn submit_partial_removal(&self, engine: &DbEngine<P>) -> sqlx::Result<()>;
}

/// Structs implementing [ItemMod] has structure similar to its sibling struct which implements [Item] but contains modified data and modification information.
pub trait ItemMod {
    /// The sibling struct which implements [Item].
    type FromItem: Item<IntoMod = Self>;

    /// Changes [Self::FromItem] to [Self] with default modification.
    fn from_item(value: &Self::FromItem) -> Self;
}

/// A trait which allows modified item data to be submitted into SQL databases.
#[async_trait::async_trait]
pub trait SubmitMod<P: SqlxPool>: ItemMod {
    /// Submits modification.
    async fn submit_mod(&self, engine: &DbEngine<P>) -> sqlx::Result<()>;
}

/// A trait which allows attachment items to be submitted into SQL database as [ItemMod].
#[async_trait::async_trait]
pub trait AttachmentItemMod<Parent: Item, Pool: SqlxPool>: ItemMod {
    /// Submit [Self] to parent item.
    async fn submit_attachment_to(
        &self,
        parent: &Parent,
        engin: &DbEngine<Pool>,
    ) -> sqlx::Result<()>;

    /// Detaches [Self] to parent item.
    async fn submit_detachment_from(
        &self,
        parent: &Parent,
        engin: &DbEngine<Pool>,
    ) -> sqlx::Result<()>;

    /// Modifies [Self].
    async fn submit_modification_with(
        &self,
        parent: &Parent,
        engin: &DbEngine<Pool>,
    ) -> sqlx::Result<()>;
}
