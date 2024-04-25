//! Handles how data interact with input and output

pub mod interface;

// use crate::data::LemmaItem;
// use crate::insertions::ToTable;
// use sqlx::Pool;

// fn read_csv(
//     path: &std::path::Path,
//     delimiter: Option<u8>,
//     terminator: Option<u8>,
// ) -> Result<Vec<LemmaItem>, csv::Error> {
//     let delim = delimiter.unwrap_or(b',');
//     let term = match terminator {
//         Some(c) => csv::Terminator::Any(c),
//         None => csv::Terminator::CRLF,
//     };
//     let mut rdr = csv::ReaderBuilder::new()
//         .delimiter(delim)
//         .terminator(term)
//         .trim(csv::Trim::All)
//         .from_path(path)?;

//     rdr.deserialize().into_iter().collect()
// }

// pub async fn import_from_csv(
//     path: &std::path::Path,
//     delimiter: Option<u8>,
//     terminator: Option<u8>,
//     db: &Pool<sqlx::Sqlite>,
// ) -> sqlx::Result<String> {
//     let mut count: i128 = 0;
//     let data = dbg!(read_csv(path, delimiter, terminator).unwrap());
//     for d in data.iter() {
//         d.insert_safe(db).await?;
//         count += 1
//     }
//     Ok(format!(
//         "{} items imported from {}.",
//         count,
//         path.as_os_str().to_str().unwrap()
//     ))
// }
