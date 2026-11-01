
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest

APP_PATH = Path("../../frontend/app.py")

def creer_table_assures():
    return pd.DataFrame({
        "age": [25, 35, 45, 55],
        "imc": [22.5, 25.0, 28.5, 31.0],
        "enfants": [0, 1, 2, 3],
        "sexe": ["female", "male", "female", "male"],
        "est_fumeur": [0, 1, 0, 1],
        "region": ["nord", "sud", "est", "ouest"],
    }, index=[1, 2, 3, 4])

def creer_metriques(mae_modele=100, mae_baseline=150):
    return {
        "r2_modele": 0.85,
        "mae_modele": mae_modele,
        "mae_baseline": mae_baseline,
        "importance_permutation": {
            "age": 0.35,
            "imc": 0.25,
            "est_fumeur": 0.40,
        },
    }

def lancer_application():
    return AppTest.from_file(str(APP_PATH)).run()

def test_chargement_application():
    app = lancer_application()
    assert not app.exception

def test_titre_application():
    app = lancer_application()
    assert any("Prédiction des charges médicales" in titre.value for titre in app.title)

def test_onglets_application():
    app = lancer_application()
    assert len(app.tabs) == 3
    assert not app.exception

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_application_avec_nouvel_assure(mock_assures, mock_metriques):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques()
    app = lancer_application()
    assert not app.exception
    assert len(app.slider) >= 1
    assert len(app.selectbox) >= 3

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_application_avec_assure_existant(mock_assures, mock_metriques):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques()
    app = lancer_application()
    app.radio[0].set_value("Assuré existant").run()
    assert not app.exception
    assert len(app.selectbox) >= 4

@patch("backend.service.predire_prime")
@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_prediction_charges(mock_assures, mock_metriques, mock_prediction):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques()
    mock_prediction.return_value = {
        "frais_estimes": 12000,
        "prime_recommandee": 13200,
    }
    app = lancer_application()
    app.button[0].click().run()
    assert not app.exception
    mock_prediction.assert_called_once()

@patch("backend.service.profils_segments")
@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_segmentation_application(mock_assures, mock_metriques, mock_segments):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques()
    mock_segments.return_value = pd.DataFrame({
        "effectif": [2, 2, 0],
        "charges_moyennes": [5000, 10000, 15000],
    })
    app = lancer_application()
    assert not app.exception
    mock_segments.assert_called_once_with(3)

@patch("backend.service.profils_segments")
@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_erreur_segmentation(mock_assures, mock_metriques, mock_segments):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques()
    mock_segments.side_effect = FileNotFoundError("Fichier absent")
    app = lancer_application()
    assert not app.exception
    assert any("Impossible de calculer les segments" in erreur.value for erreur in app.error)

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_comparaison_modele_superieur(mock_assures, mock_metriques):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques(100, 150)
    app = lancer_application()
    assert not app.exception
    assert len(app.success) >= 1

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_comparaison_modele_inferieur(mock_assures, mock_metriques):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques(200, 150)
    app = lancer_application()
    assert not app.exception
    assert len(app.warning) >= 1

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_comparaison_modele_egal(mock_assures, mock_metriques):
    mock_assures.return_value = creer_table_assures()
    mock_metriques.return_value = creer_metriques(150, 150)
    app = lancer_application()
    assert not app.exception
    assert len(app.info) >= 1

@patch("backend.service.metriques")
@patch("backend.service.lister_assures")
def test_absence_metriques(mock_assures, mock_metriques):
    mock_metriques.side_effect = FileNotFoundError()
    app = lancer_application()
    assert any("Modèle ou métriques absents" in erreur.value for erreur in app.error)
