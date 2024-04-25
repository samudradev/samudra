PRAGMA foreign_keys=off;

CREATE TABLE IF NOT EXISTS cakupan_temp (
    id INTEGER,
    tarikh_masuk TIMESTAMP,
    nama TEXT NOT NULL,
    keterangan TEXT
);

INSERT INTO cakupan_temp SELECT * FROM cakupan;

DROP TABLE cakupan;

CREATE TABLE IF NOT EXISTS cakupan (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tarikh_masuk TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nama TEXT NOT NULL,
    keterangan TEXT
);

INSERT OR IGNORE INTO cakupan SELECT * FROM cakupan_temp;

PRAGMA foreign_keys=on;
