-- Add up migration script here
CREATE TABLE IF NOT EXISTS cakupan (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tarikh_masuk TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nama TEXT NOT NULL,
    keterangan TEXT
);

CREATE TABLE IF NOT EXISTS cakupan_x_konsep (
    konsep_id INTEGER NOT NULL,
    cakupan_id INTEGER NOT NULL,
    PRIMARY KEY (konsep_id, cakupan_id),
    FOREIGN KEY (konsep_id) REFERENCES konsep(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (cakupan_id) REFERENCES cakupan(id) ON UPDATE CASCADE ON DELETE CASCADE
)