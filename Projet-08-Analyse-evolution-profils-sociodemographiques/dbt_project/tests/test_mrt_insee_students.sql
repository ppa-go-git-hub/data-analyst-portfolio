SELECT *
FROM {{ ref('mrt_insee_students') }}
WHERE gender = 'Non renseigné' AND total_insee != 0