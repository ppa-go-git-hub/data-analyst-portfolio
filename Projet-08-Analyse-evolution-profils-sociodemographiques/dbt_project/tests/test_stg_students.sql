SELECT
    user_id,
    COUNT(*) AS "occurrences",
    COUNT(DISTINCT age_group) AS "distinct AGE_GROUP count",
    COUNT(DISTINCT gender) AS "distinct GENDER count",
    COUNT(DISTINCT year_path_started) AS "distinct YEAR_PATH_STARTED count",
FROM {{ ref('stg_students') }}
GROUP BY user_id
HAVING NOT(
    COUNT(DISTINCT age_group) = 1 -- Pas de changement de tranche d'âge
AND COUNT(DISTINCT gender) = 1 -- Pas de changement de sexe
AND COUNT(DISTINCT year_path_started) = COUNT(*) -- Pas de répétition d'année de début de parcours
)