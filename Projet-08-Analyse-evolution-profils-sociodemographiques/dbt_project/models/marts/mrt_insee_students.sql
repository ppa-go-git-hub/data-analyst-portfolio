{{ config(materialized='external', format='csv') }}
SELECT
    year,
    region,
    age_group,
    gender,
    coalesce(total_insee, 0) AS total_insee,
    coalesce(total_students, 0) AS total_students
FROM {{ ref("int_insee") }} NATURAL FULL JOIN {{ ref("int_students") }}
ORDER BY year, region, age_group, gender
