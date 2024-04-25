INSERT INTO lemma (id, nama) 
    VALUES (2, "ufuk peristiwa");

INSERT INTO konsep (id, lemma_id, golongan_id, keterangan) 
    VALUES (2, 2, "NAMA", "sempadan terluar lohong hitam");

INSERT INTO cakupan_x_konsep (konsep_id, cakupan_id)
    VALUES (2, 1);

INSERT INTO cakupan_x_konsep (konsep_id, cakupan_id)
    VALUES (2, 2);

INSERT INTO kata_asing (id, nama, bahasa)
    VALUES (2, "event horizon", "english");

INSERT INTO kata_asing_x_konsep (konsep_id, kata_asing_id)
    VALUES (2, 2);