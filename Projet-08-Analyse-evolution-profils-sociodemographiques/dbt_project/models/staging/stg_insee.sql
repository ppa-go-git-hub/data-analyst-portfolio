SELECT
    year,
    CASE
        WHEN gender = 'Femmes' THEN 'Femme'
        WHEN gender = 'Hommes' THEN 'Homme'
        ELSE 'Invalide'
    END AS gender,
    region,
    age_group,
    total
FROM
    {{ ref('src_insee') }}
WHERE
        year >= {{ var('year_min') }}
    AND year <= {{ var('year_max') }}
    AND region NOT IN ('France métropolitaine', 'DOM', 'France métropolitaine et DOM')
