PRAGMA foreign_keys=off;

-- Renaming konsep to konsep_temp triggers all references of konsep to be renamed to konsep_temp even with PRAGMA foreign_keys=off
-- THEREFORE, the current method does the following:
-- 1. Copies all data from konsep into the newly created konsep_temp,
-- 2. Drops konsep table,
-- 3. Recreate konsep table,
-- 4. Copies data from konsep_temp to konsep

CREATE TEMP TABLE konsep_temp (
    id INTEGER,
    tarikh_masuk TIMESTAMP,
    lemma_id INTEGER,
    golongan_id TEXT,
    keterangan TEXT,
    tertib INTEGER
);

INSERT INTO konsep_temp SELECT * FROM konsep;

DROP TABLE konsep;

CREATE TABLE IF NOT EXISTS konsep (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tarikh_masuk TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lemma_id INTEGER NOT NULL,
    golongan_id TEXT,
    keterangan TEXT,
    tertib INTEGER,
    FOREIGN KEY (lemma_id) REFERENCES lemma(id) ON DELETE CASCADE,
    FOREIGN KEY (golongan_id) REFERENCES golongan_kata(id) ON UPDATE CASCADE ON DELETE SET DEFAULT,
    UNIQUE (lemma_id, golongan_id, keterangan)
);
INSERT INTO konsep SELECT * FROM konsep_temp;

DROP TABLE konsep_temp;

PRAGMA foreign_keys=on;

