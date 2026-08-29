SELECT
    user_id,
    path_category_name,
    age_group,
    CASE
        WHEN gender IS NULL THEN 'Non renseigné'
        WHEN gender = 'F' THEN 'Femme'
        WHEN gender = 'M' THEN 'Homme'
        ELSE 'Invalide'
    END AS gender,
    region,
    year_path_started
FROM
    {{ source('csv', 'students') }}
WHERE
        year_path_started >= {{ var('year_min') }}
    AND year_path_started <= {{ var('year_max') }}
