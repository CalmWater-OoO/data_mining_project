from pathlib import Path

from backend.config import (
    BASE,
    FICHIER_BRUT,
    FICHIER_METRIQUES,
    FICHIER_MODELE,
    RACINE,
    REQUETE_ANALYSE,
    SEED,
)


def test_racine_du_projet():
    assert RACINE == Path(__file__).resolve().parents[2]


def test_chemins_de_configuration():
    assert FICHIER_BRUT == RACINE / "data" / "raw" / "insurance.csv"
    assert BASE == RACINE / "data" / "assurance.db"
    assert FICHIER_MODELE == RACINE / "models" / "modele.joblib"
    assert FICHIER_METRIQUES == RACINE / "models" / "metriques.json"
    assert REQUETE_ANALYSE == RACINE / "backend" / "sql" / "table_analyse.sql"


def test_seed_fixe():
    assert SEED == 42
