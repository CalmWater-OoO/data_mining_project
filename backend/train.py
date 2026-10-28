"""Entraîne et sauvegarde le modèle. Usage : python -m backend.train"""
import json

import joblib
from sklearn.model_selection import cross_val_score, train_test_split

from backend.config import FICHIER_METRIQUES, FICHIER_MODELE, SEED
from backend.data import charger_brut_dans_sqlite, lire_table_analyse
from backend.model import CIBLE, VARIABLES, creer_pipeline, evaluer


def main() -> dict:
    """Exécute tout le flux : ingestion, séparation train/test, entraînement, évaluation et sauvegarde."""
    nb_lignes = charger_brut_dans_sqlite()
    table = lire_table_analyse()
    X, y = table[VARIABLES], table[CIBLE]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=SEED,
    )

    pipeline = creer_pipeline()
    mae_cv = -cross_val_score(pipeline, X_train, y_train, cv=5, scoring="neg_mean_absolute_error")
    pipeline.fit(X_train, y_train)

    metriques = evaluer(pipeline, X_train, y_train, X_test, y_test)
    metriques.update({
        "nb_demandes": nb_lignes,
        "charge_moyenne": float(y.mean()),
        "mae_cv_moyenne": float(mae_cv.mean()),
        "mae_cv_ecart_type": float(mae_cv.std()),
    })

    FICHIER_MODELE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, FICHIER_MODELE)
    FICHIER_METRIQUES.write_text(json.dumps(metriques, indent=2, ensure_ascii=False), encoding="utf-8")
    return metriques


if __name__ == "__main__":
    resultats = main()
    print(f"R2 test : {resultats['r2_modele']:.3f}")
    print(f"Erreur moyenne (MAE) Modèle : {resultats['mae_modele']:.2f} $ "
          f"(Validation Croisée : {resultats['mae_cv_moyenne']:.2f} ± {resultats['mae_cv_ecart_type']:.2f})")
    print(f"Erreur moyenne (MAE) Baseline : {resultats['mae_baseline']:.2f} $")
    print(f"Modèle sauvegardé : {FICHIER_MODELE}")