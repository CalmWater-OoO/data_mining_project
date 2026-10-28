"""Interface du backend : le frontend n'appelle que ces fonctions."""
import json
from functools import lru_cache

import joblib
import pandas as pd

from backend.config import FICHIER_METRIQUES, FICHIER_MODELE
from backend.data import lire_table_analyse
from backend.model import VARIABLES, VARIABLES_SEGMENTATION, segmenter, regle_tarifaire


@lru_cache(maxsize=1)
def _modele():
    if not FICHIER_MODELE.exists():
        raise FileNotFoundError("Modèle absent. Lancer d'abord : python -m backend.train")
    return joblib.load(FICHIER_MODELE)


def lister_assures() -> pd.DataFrame:
    return lire_table_analyse()


def predire_prime(profil: dict) -> dict:
    """Estime les frais médicaux d'un profil et applique la règle de tarification métier."""
    manquantes = set(VARIABLES) - set(profil)
    if manquantes:
        raise ValueError(f"Variables manquantes : {sorted(manquantes)}")
    estimation = float(_modele().predict(pd.DataFrame([profil])[VARIABLES])[0])
    return {"frais_estimes": estimation, "prime_recommandee": regle_tarifaire(estimation)} 


def metriques() -> dict:
    return json.loads(FICHIER_METRIQUES.read_text(encoding="utf-8"))


def profils_segments(k: int = 3) -> pd.DataFrame:
    """Profil moyen et charges moyennes de chaque segment K-means."""
    table = segmenter(lister_assures(), k)
    profils = table.groupby("segment")[VARIABLES_SEGMENTATION + ["charges"]].mean().round(2)
    profils.insert(0, "effectif", table["segment"].value_counts().sort_index())
    return profils.rename(columns={"charges": "charges_moyennes"})