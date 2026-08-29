SELECT insee_age_group, oc_age_group
FROM {{ ref('sed_matching_age_group') }}
WHERE oc_age_group IS NOT NULL