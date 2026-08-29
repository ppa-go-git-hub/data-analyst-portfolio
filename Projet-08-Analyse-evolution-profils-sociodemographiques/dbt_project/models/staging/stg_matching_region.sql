SELECT insee_region, oc_region
FROM {{ ref('sed_matching_region') }}