# Model Card : Assurance Santé (Medical Cost)

| Rubrique | Contenu | 
| ----- | ----- | 
| Usage prévu | Aider un analyste du secteur de l'assurance à estimer les frais médicaux (charges) d'un assuré à partir de ses caractéristiques. L'estimation sert à analyser les dépenses médicales et à mieux comprendre les profils associés à des frais élevés. |
| Usages à éviter | Refuser automatiquement une couverture d'assurance, pénaliser un assuré ou prendre seul une décision individuelle importante. Ne pas extrapoler à d'autres populations sans réentraîner et revalider. | 
| Modèle | Random forest qui prédit la variable charges avec 200 arbres| 
| Données | Dataset Medical Cost Personal Datasets (Kaggle), fichier insurance.csv : 1 338 observations et 7 variables; split stratifié 75/25 ; voir data_quality_card.md | 
| Baseline | Tarif unique pour tous les individus. Son erreur absolue moyenne est de 9 643$ | 
| Métriques | Erreur absolue moyenne (MAE) de 2 504$ avec un R² de 0.87. En validation croisé MAE moyenne de 2 599$ ± 142$. MAE réduit de 74% par rapport à la baseline. | 
| Seuil | Marge de sécurité de 10% : frais estimés * 1.10.  | 
| Variables importantes | Importance par permutation. Le statut fumeur est la variable la plus déterminante suivi de l'âge.  | 
| Segments | K-means avec 3 groupes. Un profil « standard » regroupe notamment des individus jeunes, avec un IMC dans la norme et des frais moyens d’environ 6 400 $. | 
| Equité | ----- | 
| Limites | Petit échantillon (1 338 individus). Données pour les Etat-Unis et donc pas représentative pour les autres population. Frais médicaux dépendent également d'autres facteurs pas présents dans cette base de donneés. | 
| Maintenance | Réentrainer si MAE devient nettement différent de 2 504$ | 
