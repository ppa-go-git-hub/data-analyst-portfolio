WITH
    all_years_path_started(year_path_started) AS (
        SELECT DISTINCT year_path_started FROM {{ ref("stg_students") }}
    ),
    all_regions(region) AS (
        SELECT DISTINCT oc_region FROM {{ ref("stg_matching_region") }}
    ),
    all_age_groups(age_group) AS (
        SELECT DISTINCT oc_age_group FROM {{ ref("stg_matching_age_group") }}
    ),
    all_genders(gender) AS (
        SELECT DISTINCT gender FROM {{ ref("stg_students") }}
    ),
    all_combinations(year_path_started, region, age_group, gender) AS (
        SELECT year_path_started, region, age_group, gender
        FROM all_years_path_started, all_regions, all_age_groups, all_genders
    )
SELECT
    year_path_started AS year,
    region,
    age_group,
    gender,
    count(user_id) AS total_students
FROM all_combinations NATURAL LEFT JOIN {{ ref("stg_students") }}
GROUP BY year_path_started, region, age_group, gender