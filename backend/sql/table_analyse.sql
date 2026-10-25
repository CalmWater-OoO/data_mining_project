
SELECT
    id_assure,
    age,
    CASE WHEN sex = 'female' THEN 'femme' ELSE 'homme' END AS sexe,
    bmi AS imc,
    children AS enfants,
    CASE WHEN smoker = 'yes' THEN 1 ELSE 0 END AS est_fumeur,
    region,
    charges
FROM assurance
GROUP BY age, sex, bmi, children, smoker, region, charges;