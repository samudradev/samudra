SELECT 
    COUNT(DISTINCT lemma.id) AS lemmas,
    COUNT(DISTINCT konsep.id) AS konseps,
    COUNT(DISTINCT golongan_kata.id) as golongan_katas,
    COUNT(DISTINCT cakupan.id) as cakupans,
    COUNT(DISTINCT kata_asing.id) as kata_asings
FROM lemma, konsep, golongan_kata, cakupan, kata_asing