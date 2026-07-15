SELECT
    concepticon_id, concepticon_gloss, gloss, max(c) AS ngloss
FROM (
    SELECT
        p.cldf_id AS concepticon_id,
        p.cldf_name AS concepticon_gloss,
        c.cldf_name AS gloss,
        count(c.cldf_id) AS c
    FROM
        parametertable AS p,
        `concepts.csv` AS c,
        formtable AS f
    WHERE
        c.cldf_parameterreference = p.cldf_id AND
        f.concept_id = c.cldf_id AND
        f.cldf_languagereference = 'english'
    GROUP BY p.cldf_id, c.cldf_name
) AS q
WHERE
    lower(concepticon_gloss) != lower(gloss) AND
    cast(concepticon_id as int) != 0
GROUP BY concepticon_id
HAVING ngloss > 5
ORDER BY cast(concepticon_id AS int) LIMIT 5;