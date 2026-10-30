# Note de synthèse : un modèle pour mieux estimer les frais médicaux des assurés

__Pour :__ Compagnie d'assurance santé __De :__ Equipe SEP Conseil 
__Document :__ Synthèse du projet Data Mining 1

## La décision que nous vous demandons 

Utiliser le modèle Random Forest comme un outil d'aide à l'estimation des frais médicaux. Pour mieux anticiper les dépenses associés aux différents profils d'assurés. Cette estimation doit rester indicative et ne doit pas constituer le seul critère de décision. 

## Votre question 

Comment une compagnie d'assurance santé peut-elle mieux anticiper les frais médicaux de ses assurés grâce aux caractéristiques individuelles de leurs assurés ? 

## Ce que nous avons trouvé

1. Un modèle globalement performant. A partir de 1 338 observations, le modèle obtient une MAE de 2 504$ avec un R² de 0.88 sur la partie test du jeu de données.

2. Une amélioration importante par rapport à baseline. Sans modèle, la prédiction sur la moyenne des frais médicaux donne une MAE de 9 644$ et le modèle réduit cette erreur de 74%.

3. Le statut de fumeur et l'âge sont les variables les plus importantes. Avec l'analyse par permutation on vois que le statut de fumeur et l'âge contribue le plus à la qualité des prédictions. 

4. 3 trois profils d'assurés se distinguent. La segmentation K-means identifie trois groupes : un groupe plus jeune avec pas trop de frais, un groupe plus âgé avec des frais moyens et un groupe présentant des frais élevés.

## Nos résultats chiffrés 

Sur le jeu de test, le modèle obtient les résultats suivants : 

| Indicateur | Résultat | 
| ----- | ----- | 
| Nombre d'individu | 1 338 | 
| MAE de la baseline | 9 643,85$ | 
| MAE du Random Forest | 2 504,35$ | 
| R² du Random Forest | 0.878 | 
| MAE moyenne en validation croisée (5 plis) | 2 598,93$ | 
| Ecart-type de la MAE en validation croisée | 142,96$ | 
| Réduction de la MAE par rapport à la baseline | Environ 74% | 

Le modèle applique aussi une majoration de 10% à l'estimation brute afin de proposer une prime indicative. 

## Ce que le modèle ne sait pas faire 

1. Il ne prédit pas parfaitement les dépenses individuelles : une MAE de 2 504$ signifie que les estimations présentent encore un écart avec les frais réels.

2. Les données sont limitées : le dataset a 1 338 observations d'assurés américains. Les résultats ne peuvent pas être généralisés à d'autres pays ou populations.

3. Certaines variables peuvent soulever des questions d'équité : l'âge et le statut de fumeur jouent un rôle important dans les prédictions. 

4. Les frais médicaux peuvent dépendre d'autres facteurs. certaines informations susceptibles d'influencer les dépenses ne sont pas disponibles dans le dataset. 

5. La segmentation dépend des variables choisies : les frais médicaux étant eux-mêmes utilisés dans le K-means, les groupes obtenus ne constituent pas des catégories sans risque. 

## Nos recommandations 

1. Utiliser le Random Forest comme outil d'aide à l'estimation et non comme outil de décision automatique

2. Evaluer les performances du modèle sur des nouvelles données afin de vérifier que sa précision se maintient dans le temps

3. Etudier les écarts d'erreur entre les différentes tranches d'âge et les autres groupes d'assurés.

4. Envisager un réentrainement si les performances se dégradent ou si les caractéristiques des données évoluent.

## Comment suivre les résultats 

| Indicateur | Fréquence proposée | Alerte si | Qui | 
| ----- | ----- | ----- | ----- |
| MAE des prédictions | Mensuelle | Elle devient trop différentes de la MAE de référence de 2 504$ | Service de tarification |
| Ecart de MAE selon les tranches d'âge | Trimestrielle | Un écart important apparaît entre les différentes tranches | Service de conformité |
| Répartition des profils d'assurés | Trimestrielle | La répartition des segments évolue fortement | Service d'analyse des données |