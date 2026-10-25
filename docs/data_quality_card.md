# Data Quality Card : Assurance Santé (Medical Cost)

| Question | Réponse | 
| ----- | ----- | 
| Unité d'observation | Un assuré principal aux États-Unis. | 
| Source, licence, lien | [Medical Cost Personal Datasets (Kaggle)](https://www.kaggle.com/datasets/mirichoi0218/insurance). | 
| Période et population couvertes | Adultes assurés aux USA de 18 à 64 ans. | 
| Taille | 1 338 lignes × 7 variables + cible. | 
| Cible | `charges` (frais médicaux facturés, variable continue). | 
| Valeurs manquantes | 0 dans l'ensemble du dataset. | 
| Doublons | 1 doublon strict (géré par le `GROUP BY` dans la requête SQL). | 
| Valeurs aberrantes ou impossibles | Aucune valeur aberrante mathématiquement. Forte asymétrie sur `charges` | 
| Modalités jouant le rôle d'un manquant | Aucune. | 
| Classes déséquilibrées | La variable `smoker` est déséquilibrée (1064 non-fumeurs pour 274 fumeurs). | 
| Variables à risque de fuite | Aucune. Toutes les caractéristiques sont connues au moment de la souscription. | 
| Variables sensibles | Sexe, âge, IMC, statut fumeur. | 
| Biais de sélection | Les seniors et les personnes sans assurance sont exclus. | 
| Données personnelles | Données synthétiques et anonymisées. | 
| Variables les plus utiles et pourquoi | L'interaction entre le statut fumeur et l'IMC, qui a un impact critique sur le risque de santé. | 
| Ce que les données ne permettent pas de dire | Les antécédents médicaux précis, la gravité d'une pathologie en cours, l'intensité du tabagisme, et les revenus. | 