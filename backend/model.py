"""Modèles : Random Forest (supervisé) et K-means (non supervisé)."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from backend.config import SEED

VARIABLES_NUM = ["age", "imc", "enfants"]
VARIABLES_CAT = ["sexe", "est_fumeur", "region"]
VARIABLES = VARIABLES_NUM + VARIABLES_CAT
CIBLE = "charges"
VARIABLES_SEGMENTATION = ["age", "imc", "charges"]


def creer_pipeline() -> Pipeline:
    preparation = ColumnTransformer(
        [("num", StandardScaler(), VARIABLES_NUM),
         ("cat", OneHotEncoder(handle_unknown="ignore"), VARIABLES_CAT)]
    )
    foret = RandomForestRegressor(
        n_estimators=200, min_samples_leaf=4, random_state=SEED, n_jobs=-1,
    )
    return Pipeline([("preparation", preparation), ("foret", foret)])


def regle_tarifaire(estimation_brute: float) -> float:
    """Applique une marge de sécurité de 10% sur l'estimation pour fixer la prime."""
    return float(estimation_brute * 1.10)


def calculer_mae(y_vrai, predictions) -> float:
    """Calcule l'Erreur Absolue Moyenne (MAE) en dollars."""
    return float(mean_absolute_error(y_vrai, predictions))


def evaluer(pipeline: Pipeline, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Évalue le modèle sur le jeu de test et renvoie les métriques."""
    predictions = pipeline.predict(X_test)
    
    baseline = DummyRegressor(strategy="mean")
    baseline.fit(X_train, y_train)
    predictions_baseline = baseline.predict(X_test)
    
    importances = permutation_importance(
        pipeline, X_test, y_test, scoring="neg_mean_absolute_error", n_repeats=10, random_state=SEED,
    )
    
    return {
        "r2_modele": float(r2_score(y_test, predictions)),
        "mae_modele": calculer_mae(y_test, predictions),
        "mae_baseline": calculer_mae(y_test, predictions_baseline),
        "importance_permutation": dict(
            sorted(zip(X_test.columns, importances.importances_mean.round(4).tolist()),
                   key=lambda paire: paire[1])
        ),
    }


def segmenter(table: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """K-means sur variables standardisées. Renvoie la table avec une colonne `segment`."""
    valeurs = StandardScaler().fit_transform(table[VARIABLES_SEGMENTATION])
    segments = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(valeurs)
    return table.assign(segment=segments)