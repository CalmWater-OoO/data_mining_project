# SEP Conseil et Assurance : Estimation Tarifaire

## Question business

Comment une compagnie d’assurance santé peut-elle mieux anticiper les frais médicaux individuels à partir des caractéristiques personnelles d’un assuré, sans utiliser son diagnostic, afin d’éclairer l’analyse des dépenses et des profils d’assurés ?

## Résultats 

| Stratégie tarifaire | Erreur moyenne d'estimation (MAE) |
|---|---|
| Tarif unique  | 9 643 $ |
| Random Forest | 2 504 $ |
| **Random Forest + Marge de sécurité (+10%)** | **Prime recommandée au conseiller** |

- **R² de 0,87** sur le jeu de test : un résultat encourageant pour estimer les frais médicaux à partir des variables disponibles.
- Modèle stable : l'erreur moyenne en validation croisée est de 2 599 $ ± 142 $.
- La variable la plus déterminante est le **statut fumeur** suivie de **l'âge**, ce qui valide la logique métier.
- L'exploration K-means (3 segments) met en évidence des profils contrastés, dont un groupe plus jeune avec des frais moyens d'environ 6 400 $ et un groupe aux frais moyens plus élevés.

## Lancer le projet

Le projet a été réalisée avec la version 3.14.10 de python téléchargeable à l'URL : https://www.python.org/downloads/

Pour lancer le projet vous devez suivre les étapes ci-dessous dans l'ordre:

```bash
py --version # cette commande est censée renvoyer Python : 3.14.10 ou une version ultérieure
py -m venv .venv && source .venv/Scripts/activate   # Windows (Git Bash)   
pip install -r requirements.txt
py -m backend.train                # SQLite + table d'analyse SQL + Entraînement 
py -m pytest                       # Lance les tests avec pytest-cov (100% coverage)
py -m streamlit run frontend/app.py
```

## Architecture : backend et frontend séparés


```
backend/                 logique métier (aucun import de streamlit)
  config.py              chemins, seed, paramètres
  sql/table_analyse.sql  table d'analyse construite et nettoyée en SQL
  data.py                fichier brut -> SQLite -> table d'analyse
  model.py               Random Forest Regressor, évaluation (MAE/R²), K-means
  train.py               entraînement et sauvegarde du modèle
  service.py             SEULE interface appelée par le frontend
frontend/
  app.py                 Streamlit : affichage et interaction uniquement
tests/                   tests du backend et démarrage de l'appli
docs/                    Data Quality Card, Model Card, note de synthèse, journal IA, plan de soutenance
data/raw/                données brutes (insurance.csv - jamais modifiées)
```

## Limites

- Le projet s'appuie sur 1 338 assurés des États-Unis. Cette base nous a permis de construire et d'évaluer un premier modèle. Pour plus de précision nous pourions tester celui-ci sur des données plus récentes et d'autres populations 
- Les données ne comportent pas de diagnostic : le modèle répond bien à notre objectif d'estimer les frais à partir des caractéristiques disponibles, mais il ne vise pas à prédire l'état de santé.
- L'âge, le sexe et le statut fumeur contribuent aux prédictions. Pour envisager un usage réel, une prochaine étape serait de comparer les erreurs entre différents groupes et de discuter avec les professionnels des variables à retenir.
- La majoration de 10 % illustre comment transformer une estimation en recommandation indicative. Le choix d'un tarif réel demanderait une validation métier et actuarielle complémentaire.
- Les segments K-means décrivent les groupes présents dans les données, notamment à partir des frais observés. Ils apportent un dimension exploratoire et ne constituent pas une classification prédictive pour un nouvel assuré.
- Le modèle constitue une aide à l'analyse, et non une décision automatique.