INSERT INTO lemma (id, nama) 
    VALUES (1, "cakera tokokan");

INSERT INTO golongan_kata (id, nama, keterangan) 
    VALUES ("NAMA", "kata nama", "kata yang memberi nama pada benda");

INSERT INTO konsep (id, lemma_id, golongan_id, keterangan) 
    VALUES (1, 1, "NAMA", "gas-gas dan debu yang mengelilingi lohong hitam");

INSERT INTO cakupan (id, nama, keterangan)
    VALUES (1, "Astrofizik", NULL);

INSERT INTO cakupan_x_konsep (konsep_id, cakupan_id)
    VALUES (1, 1);

INSERT INTO cakupan (id, nama, keterangan)
    VALUES (2, "Teori Relativiti", NULL);

INSERT INTO cakupan_x_konsep (konsep_id, cakupan_id)
    VALUES (1, 2);

INSERT INTO kata_asing (id, nama, bahasa)
    VALUES (1, "accretion disk", "english");

INSERT INTO kata_asing_x_konsep (konsep_id, kata_asing_id)
    VALUES (1, 1);

INSERT INTO konsep (id, lemma_id, golongan_id, keterangan) 
    VALUES (2, 1, "NAMA", "cakera yang ditokok tambah (contoh)");

INSERT INTO cakupan (id, nama, keterangan)
    VALUES (3, "Umum", NULL);

INSERT INTO cakupan_x_konsep (konsep_id, cakupan_id)
    VALUES (2, 3);
