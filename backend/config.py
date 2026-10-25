from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
FICHIER_BRUT = RACINE / "data" / "raw" / "insurance.csv"
BASE = RACINE / "data" / "assurance.db"
FICHIER_MODELE = RACINE / "models" / "modele.joblib"
FICHIER_METRIQUES = RACINE / "models" / "metriques.json"
REQUETE_ANALYSE = RACINE / "backend" / "sql" / "table_analyse.sql"

SEED = 42