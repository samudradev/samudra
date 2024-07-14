SELECT
    *
FROM
    (SELECT COUNT(DISTINCT lemma.id) as lemmas FROM lemma),
    (SELECT COUNT(DISTINCT konsep.id) as konseps FROM konsep),
    (SELECT COUNT(DISTINCT golongan_kata.id) as golongan_katas FROM golongan_kata),
    (SELECT COUNT(DISTINCT cakupan.id) as cakupans FROM cakupan),
    (SELECT COUNT(DISTINCT kata_asing.id) as kata_asings FROM kata_asing)