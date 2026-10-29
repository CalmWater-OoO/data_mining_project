# Model Card : Assurance Santé (Medical Cost)

| Rubrique | Contenu | 
| ----- | ----- | 
| Usage prévu | Aider un analyste du secteur de l'assurance à estimer les frais médicaux (charges) d'un assuré à partir de ses caractéristiques. L'estimation sert à analyser les dépenses médicales et à mieux comprendre les profils associés à des frais élevés. |
| Usages à éviter | Refuser automatiquement une couverture d'assurance, pénaliser un assuré ou prendre seul une décision individuelle importante. Ne pas extrapoler à d'autres populations sans réentraîner et revalider. | 
| Modèle | Random forest | 
| Données | Dataset Medical Cost Personal Datasets (Kaggle), fichier insurance.csv : 1 338 observations et 7 variables; split stratifié 75/25 ; voir data_quality_card.md | 
| Baseline | Prédiction constante égale à la médiane des frais médicaux du jeu d'entraînement. Cette baseline permet d'évaluer l'intérêt du modèle par rapport à une prédiction simple. | 
| Métriques | ----- | 
| Seuil | ----- | 
| Variables importantes | ----- | 
| Segments | ----- | 
| Equité | ----- | 
| Limites | ----- | 
| Maintenance | ----- | 
