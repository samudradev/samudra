/// For values automatically generated by database.
///
/// It works similar to [Option] but conveys a clearer meaning.
#[derive(Clone, serde::Serialize, serde::Deserialize)]
#[serde(untagged)]
pub enum AutoGen<T> {
    /// The value is already provided by the database
    Known(T),
    /// The value is not yet provided by the database
    Unknown,
}

impl<T: Copy> Copy for AutoGen<T> {}

impl<T: PartialEq> PartialEq for AutoGen<T> {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            // We assume different unknowns are the same value
            (Self::Unknown, Self::Unknown) => true,
            (Self::Known(l0), Self::Known(r0)) => l0 == r0,
            _ => core::mem::discriminant(self) == core::mem::discriminant(other),
        }
    }
}

impl<T> From<AutoGen<T>> for Option<T> {
    fn from(value: AutoGen<T>) -> Option<T> {
        match value {
            AutoGen::Known(v) => Some(v),
            AutoGen::Unknown => None,
        }
    }
}

impl<T, DB: sqlx::Database> sqlx::Encode<'_, DB> for AutoGen<T>
where
    T: for<'a> sqlx::Encode<'a, DB>,
    Self: Copy,
    Option<T>: for<'a> sqlx::Encode<'a, DB>,
{
    fn encode_by_ref(
        &self,
        buf: &mut <DB as sqlx::database::HasArguments<'_>>::ArgumentBuffer,
    ) -> sqlx::encode::IsNull {
        <Option<T> as sqlx::Encode<'_, DB>>::encode_by_ref(&(*self).into(), buf)
    }
}

impl<T, DB: sqlx::Database> sqlx::Type<DB> for AutoGen<T>
where
    T: sqlx::Type<DB>,
{
    fn type_info() -> DB::TypeInfo {
        <Option<T> as sqlx::Type<DB>>::type_info()
    }
}
