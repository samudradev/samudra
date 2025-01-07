//! Contains general modification structs and enums.

use std::fmt::Display;

use crate::engine::{DbEngine, SqlxPool};
use crate::io::interface::{AttachmentItemMod, Item, ItemMod};
use crate::items::konsep::KonsepMod;

use schema::items::cakupan::Cakupan as CakupanItem;
use schema::items::kata_asing::KataAsing as KataAsingItem;
use schema::items::konsep::Konsep as KonsepItem;
use schema::items::lemma::Lemma;
use schema::metatype::AutoGen;

use itertools::Itertools;
use tracing::instrument;

/// [ItemMod] fields.
#[derive(Clone, PartialEq)]
pub enum FieldMod<T> {
    New(T),
    Fixed(T),
}

impl<T> FieldMod<T> {
    pub fn value(&self) -> &T {
        match self {
            FieldMod::New(v) => v,
            FieldMod::Fixed(v) => v,
        }
    }
}

impl<T: PartialEq> FieldMod<T> {
    pub fn compare(old: T, new: T) -> FieldMod<T> {
        if old == new {
            FieldMod::Fixed(old)
        } else {
            FieldMod::New(new)
        }
    }
}

/// [ItemMod] attachment fields.
///
/// An attachment field is indicated by a vector of children [Items](Item).
/// The children items in this struct implements [ItemMod].
#[derive(Clone, PartialEq)]
pub struct AttachmentMod<A: ItemMod> {
    pub attached: Vec<A>,
    pub detached: Vec<A>,
    pub modified: Vec<A>,
}

impl<A> AttachmentMod<A>
where
    A: ItemMod,
{
    #[instrument(skip_all)]
    pub async fn submit_changes_with<Parent, Pool>(
        &self,
        parent: &Parent,
        engine: &DbEngine<Pool>,
    ) -> sqlx::Result<()>
    where
        A: ItemMod + AttachmentItemMod<Parent, Pool>,
        Parent: Item,
        Pool: SqlxPool,
    {
        for attached in self.attached.iter() {
            attached.submit_attachment_to(parent, engine).await?;
        }
        for detached in self.detached.iter() {
            detached.submit_detachment_from(parent, engine).await?;
        }
        for modified in self.modified.iter() {
            modified.submit_modification_with(parent, engine).await?;
        }
        Ok(())
    }

    pub fn empty() -> AttachmentMod<A> {
        AttachmentMod {
            attached: vec![],
            detached: vec![],
            modified: vec![],
        }
    }
}

impl<A: ItemMod, I: Item<IntoMod = A>> From<Vec<I>> for AttachmentMod<A> {
    fn from(value: Vec<I>) -> Self {
        AttachmentMod {
            attached: Vec::from_iter(value.iter().map(|item| item.modify_into(item).unwrap())),
            detached: vec![],
            modified: vec![],
        }
    }
}

/// A trait which compares vectors of children for use with [AttachmentMod].
pub trait CompareAttachable<I: PartialEq + Clone + Item<IntoMod = A>, A: ItemMod<FromItem = I>> {
    fn items(&self) -> Vec<I>;

    fn find_attached(&self, other: &Vec<I>) -> Vec<A> {
        Vec::clone(other)
            .into_iter()
            .filter(|item| !self.items().contains(item))
            .map(|item| A::from_item(&item))
            .collect_vec()
    }

    fn find_detached(&self, other: &Vec<I>) -> Vec<A> {
        Vec::clone(&self.items())
            .into_iter()
            .filter(|item| !other.contains(item))
            .map(|item| A::from_item(&item))
            .collect_vec()
    }

    fn find_modified(&self, _other: &Vec<I>) -> Vec<A> {
        Vec::new()
    }

    fn compare_attachment(&self, other: Vec<I>) -> AttachmentMod<A> {
        AttachmentMod {
            attached: self.find_attached(&other),
            detached: self.find_detached(&other),
            modified: self.find_modified(&other),
        }
    }
}

impl<I: Copy + Clone + PartialEq> CompareAttachable<KonsepItem<I>, KonsepMod<I>> for Lemma<I> {
    fn items(&self) -> Vec<KonsepItem<I>> {
        Vec::clone(&self.konseps)
    }
    fn find_attached(&self, other: &Vec<KonsepItem<I>>) -> Vec<KonsepMod<I>> {
        Vec::clone(other)
            .into_iter()
            .filter(|item| item.id == AutoGen::Unknown)
            .map(|item| KonsepMod::from_item(&item))
            .collect_vec()
    }
    fn find_detached(&self, other: &Vec<KonsepItem<I>>) -> Vec<KonsepMod<I>> {
        let other_ids = Vec::clone(other)
            .into_iter()
            .filter(|item| item.id != AutoGen::Unknown)
            .map(|item| item.id)
            .collect_vec();
        Vec::clone(&self.items())
            .into_iter()
            .filter(|item| !other_ids.contains(&item.id))
            .map(|item| KonsepMod::from_item(&item))
            .collect_vec()
    }
    fn find_modified(&self, other: &Vec<KonsepItem<I>>) -> Vec<KonsepMod<I>> {
        let detached_id = self
            .find_detached(other)
            .iter()
            .map(|item| item.id)
            .collect_vec();
        let old = Vec::clone(&self.items())
            .into_iter()
            .filter(|item| !detached_id.contains(&item.id))
            .sorted_by(|a, b| {
                a.keterangan
                    .partial_cmp(&b.keterangan)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
        let new = Vec::clone(other)
            .into_iter()
            .filter(|item| item.id != AutoGen::Unknown)
            .sorted_by(|a, b| {
                a.keterangan
                    .partial_cmp(&b.keterangan)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
        dbg!(old.clone().map(|i| i.keterangan).collect_vec());
        dbg!(new.clone().map(|i| i.keterangan).collect_vec());
        assert_eq!(
            old.clone().collect_vec().len(),
            new.clone().collect_vec().len(),
            "The length of potentially modified items does not match the length of old items. Perhaps you forgot to supply the ID of the modified KonsepItem."
        );
        old.zip(new)
            .map(|(o, n)| o.modify_into(&n).expect("Error"))
            .collect_vec()
    }
}

#[cfg(test)]
mod test {
    // FIX: Assert eq no longer works because we no longer impl Debug
    use super::*;
    use crate::io::interface::{FromView, SubmitMod};
    use crate::items::lemma::LemmaMod;
    use crate::views::LemmaWithKonsepView;
    use tracing_test::traced_test;

    #[sqlx::test]
    #[traced_test]
    fn test_new_lemma(pool: sqlx::Pool<sqlx::Sqlite>) -> Result<(), sqlx::Error> {
        let new = Lemma {
            id: AutoGen::Unknown,
            lemma: "cakera tokokan".into(),
            konseps: vec![],
        };
        LemmaMod::from_item(&new).submit_mod(&pool).await?;
        let views = LemmaWithKonsepView::query_lemma("cakera tokokan".into(), &pool).await?;
        let data = Lemma::from_views(&views);
        assert_eq!(data, vec![new]);
        Ok(())
    }

    #[sqlx::test(fixtures("lemma"))]
    #[traced_test]
    fn test_diff_handling(pool: sqlx::Pool<sqlx::Sqlite>) -> Result<(), sqlx::Error> {
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        let old = data
            .first()
            .expect("Vec<LemmaDataRepr> is zero sized")
            .to_owned();
        assert_eq!(&old.konseps.len(), &1);
        let new: Lemma = Lemma {
            id: AutoGen::Known(1),
            lemma: "cakera tokokan".into(),
            konseps: vec![
                KonsepItem {
                    id: AutoGen::Known(1),
                    keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec!["Astrofizik".into(), "Teori Relativiti".into()],
                    kata_asing: vec![KataAsingItem {
                        nama: "accretion disk".into(),
                        bahasa: "english".into(),
                    }],
                },
                KonsepItem {
                    id: AutoGen::Unknown,
                    keterangan: "konsep baharu yang tiada kena mengena".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
            ],
        };
        old.modify_into(&new).unwrap().submit_mod(&pool).await?;
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        assert_eq!(data, vec![new]);
        Ok(())
    }

    #[test]
    #[traced_test]
    fn test_diff_handling_detach_konsep() -> Result<(), Box<dyn std::error::Error>> {
        let lemma_1 = Lemma {
            id: AutoGen::Known(1),
            lemma: "cubaan".into(),
            konseps: vec![
                KonsepItem {
                    id: AutoGen::Known(1),
                    keterangan: "cubaan simpan 1/2".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
                KonsepItem {
                    id: AutoGen::Known(2),
                    keterangan: "cubaan padam".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
                KonsepItem {
                    id: AutoGen::Known(3),
                    keterangan: "cubaan simpan 2/2".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
            ],
        };
        let lemma_2 = Lemma {
            id: AutoGen::Known(1),
            lemma: "cubaan".into(),
            konseps: vec![
                KonsepItem {
                    id: AutoGen::Known(1),
                    keterangan: "cubaan simpan 1/2".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
                KonsepItem {
                    id: AutoGen::Known(3),
                    keterangan: "cubaan simpan 2/2".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec![],
                    kata_asing: vec![],
                },
            ],
        };
        let attachment_mod = lemma_1.compare_attachment(lemma_2.konseps);
        assert_eq!(
            attachment_mod.detached,
            vec![KonsepMod {
                id: AutoGen::Known(2),
                keterangan: FieldMod::Fixed("cubaan padam".into()),
                golongan_kata: FieldMod::Fixed("kata nama".into()),
                cakupans: AttachmentMod::empty(),
                kata_asing: AttachmentMod::empty()
            }]
        );
        assert_eq!(
            attachment_mod.modified,
            vec![
                KonsepMod {
                    id: AutoGen::Known(1),
                    keterangan: FieldMod::Fixed("cubaan simpan 1/2".into()),
                    golongan_kata: FieldMod::Fixed("kata nama".into()),
                    cakupans: AttachmentMod::empty(),
                    kata_asing: AttachmentMod::empty(),
                },
                KonsepMod {
                    id: AutoGen::Known(3),
                    keterangan: FieldMod::Fixed("cubaan simpan 2/2".into()),
                    golongan_kata: FieldMod::Fixed("kata nama".into()),
                    cakupans: AttachmentMod::empty(),
                    kata_asing: AttachmentMod::empty(),
                },
            ]
        );
        assert!(false);
        Ok(())
    }

    #[sqlx::test(fixtures("lemma"))]
    fn test_diff_handling_detach_cakupan(
        pool: sqlx::Pool<sqlx::Sqlite>,
    ) -> Result<(), sqlx::Error> {
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        let old = data
            .first()
            .expect("Vec<LemmaDataRepr> is zero sized")
            .to_owned();
        assert_eq!(&old.konseps.len(), &1);
        let new: Lemma = Lemma {
            id: AutoGen::Known(1),
            lemma: "cakera tokokan".into(),
            konseps: vec![KonsepItem {
                id: AutoGen::Known(1),
                keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
                golongan_kata: "kata nama".into(),
                cakupans: vec!["Astrofizik".into()],
                kata_asing: vec![KataAsingItem {
                    nama: "accretion disk".into(),
                    bahasa: "english".into(),
                }],
            }],
        };
        old.modify_into(&new).unwrap().submit_mod(&pool).await?;
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        assert_eq!(
            data.first()
                .expect("Here?")
                .konseps
                .first()
                .expect("Konsep")
                .cakupans,
            vec!["Astrofizik".into()]
        );
        Ok(())
    }
    #[sqlx::test(fixtures("lemma"))]
    fn test_diff_handling_detach_kata_asing(
        pool: sqlx::Pool<sqlx::Sqlite>,
    ) -> Result<(), sqlx::Error> {
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        let old = data
            .first()
            .expect("Vec<LemmaDataRepr> is zero sized")
            .to_owned();
        assert_eq!(&old.konseps.len(), &1);
        let new: Lemma = Lemma {
            id: AutoGen::Known(1),
            lemma: "cakera tokokan".into(),
            konseps: vec![KonsepItem {
                id: AutoGen::Known(1),
                keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
                golongan_kata: "kata nama".into(),
                cakupans: vec!["Astrofizik".into(), "Teori Relativiti".into()],
                kata_asing: vec![],
            }],
        };
        old.modify_into(&new).unwrap().submit_mod(&pool).await?;
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        assert_eq!(data, vec![new]);
        Ok(())
    }
    #[sqlx::test(fixtures("lemma_w_2_konseps"))]
    fn test_diff_handling_attach_cakupan(
        pool: sqlx::Pool<sqlx::Sqlite>,
    ) -> Result<(), sqlx::Error> {
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);
        let old = data
            .first()
            .expect("Vec<LemmaDataRepr> is zero sized")
            .to_owned();
        assert_eq!(&old.konseps.len(), &2);
        let new: Lemma = Lemma {
            id: AutoGen::Known(1),
            lemma: "cakera tokokan".into(),
            konseps: vec![
                KonsepItem {
                    id: AutoGen::Known(1),
                    keterangan: "gas-gas dan debu yang mengelilingi lohong hitam".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec!["Astrofizik".into(), "Teori Relativiti".into()],
                    kata_asing: vec![],
                },
                KonsepItem {
                    id: AutoGen::Known(2),
                    keterangan: "cakera yang ditokok tambah (contoh)".into(),
                    golongan_kata: "kata nama".into(),
                    cakupans: vec!["Umum".into(), "Tidak Umum".into()],
                    kata_asing: vec![],
                },
            ],
        };
        old.modify_into(&new).unwrap().submit_mod(&pool).await?;
        let view = LemmaWithKonsepView::query_all(&pool).await?;
        let data = Lemma::from_views(&view);

        assert_eq!(data, vec![new]);
        Ok(())
    }
    #[test]
    fn test_compare_attachable() {
        let old = KonsepItem {
            id: AutoGen::Unknown,
            keterangan: String::default(),
            golongan_kata: String::default(),
            cakupans: vec!["a".into(), "b".into(), "c".into()],
            kata_asing: vec![KataAsingItem {
                nama: "new".into(),
                bahasa: "en".into(),
            }],
        };
        let changes_cakupan: AttachmentMod<CakupanItem> =
            old.compare_attachment(vec!["a".into(), "b".into(), "d".into()]);
        assert_eq!(
            changes_cakupan,
            AttachmentMod {
                attached: vec!["d".into()],
                detached: vec!["c".into()],
                modified: vec![]
            }
        );
        let changes_kata_asing: AttachmentMod<KataAsingItem> = old.compare_attachment(vec![]);
        assert_eq!(
            changes_kata_asing,
            AttachmentMod {
                attached: vec![],
                detached: vec![KataAsingItem {
                    nama: "new".into(),
                    bahasa: "en".into()
                }],
                modified: vec![]
            }
        )
    }
}
