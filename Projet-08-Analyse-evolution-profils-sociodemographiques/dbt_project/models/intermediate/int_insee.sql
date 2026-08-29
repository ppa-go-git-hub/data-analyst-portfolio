SELECT
    year,
    oc_region AS region,
    oc_age_group AS age_group,
    gender,
    coalesce(sum(total), 0) AS total_insee
FROM {{ ref("stg_insee") }} insee
JOIN {{ ref("stg_matching_region") }} ON insee.region = insee_region
JOIN {{ ref("stg_matching_age_group") }} ON insee.age_group = insee_age_group
GROUP BY year, oc_region, oc_age_group, gender