# SEP Conseil et Assurance : Estimation Tarifaire

## Question business



## Résultats 

| Stratégie tarifaire | Erreur moyenne d'estimation (MAE) |
|---|---|
| Tarif unique  | 9 643 $ |
| Random Forest | 2 504 $ |
| **Random Forest + Marge de sécurité (+10%)** | **Prime recommandée au conseiller** |

- **R² de 0,87** sur le jeu de test, prouvant l'excellente fiabilité du modèle.
- Modèle stable : l'erreur moyenne en validation croisée est de 2 599 $ ± 142 $.
- La variable la plus déterminante est le **statut fumeur** suivie de **l'âge**, ce qui valide la logique métier.
- L'exploration K-means (3 segments) identifie parfaitement les "profils standards" (jeunes, IMC normal, frais ~6 400 $) face aux profils à haut risque.

## Lancer le projet

Suivre les étapes ci-dessous dans l'ordre:

```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows (Git Bash)   
pip install -r requirements.txt
python -m backend.train                # SQLite + table d'analyse SQL + Entraînement 
python -m pytest                       # Lance les tests avec pytest-cov (100% coverage)
python -m streamlit run frontend/app.py
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