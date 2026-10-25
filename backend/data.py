"""Accès aux données : fichier brut -> SQLite -> table d'analyse."""
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


from backend.config import BASE, FICHIER_BRUT, REQUETE_ANALYSE

def charger_brut_dans_sqlite(fichier: Path = FICHIER_BRUT, base: Path = BASE) -> int:
    """Charge le CSV brut dans la base SQLite."""
    if not fichier.exists():
        raise FileNotFoundError(f"Fichier brut introuvable : {fichier}")
    brut = pd.read_csv(fichier)
    # Ajout d'un ID unique
    brut.insert(0, "id_assure", range(1, len(brut) + 1))
    
    base.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(base)) as con:
        brut.to_sql("assurance", con, if_exists="replace", index=False)
    
    return len(brut)

def lire_table_analyse(base: Path = BASE) -> pd.DataFrame:
    """Construit la table d'analyse avec la requête SQL versionnée dans backend/sql/."""
    if not base.exists():
        raise FileNotFoundError(f"Base introuvable : {base}. Lancer d'abord : python -m backend.train")
    with closing(sqlite3.connect(base)) as con:
        return pd.read_sql(REQUETE_ANALYSE.read_text(encoding="utf-8"), con)


