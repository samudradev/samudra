-- Add up migration script here
CREATE TABLE IF NOT EXISTS kata_asing (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tarikh_masuk TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nama TEXT NOT NULL,
    bahasa TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kata_asing_x_konsep (
    konsep_id INTEGER NOT NULL,
    kata_asing_id INTEGER NOT NULL,
    PRIMARY KEY (konsep_id, kata_asing_id),
    FOREIGN KEY (konsep_id) REFERENCES konsep(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (kata_asing_id) REFERENCES kata_asing(id) ON UPDATE CASCADE ON DELETE CASCADE
)