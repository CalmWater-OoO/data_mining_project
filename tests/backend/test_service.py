import json
import pandas as pd
import pytest
from backend import service


def test_modele_introuvable(tmp_path, monkeypatch):
    monkeypatch.setattr(service, "FICHIER_MODELE", tmp_path / "absent.joblib")
    with pytest.raises(FileNotFoundError):
        service._modele()

def test_lister_assures():
    resultat = service.lister_assures()
    assert isinstance(resultat, pd.DataFrame)
    assert not resultat.empty


def test_predire_prime():
    resultat = service.predire_prime({
        "age": 30,
        "imc": 25,
        "enfants": 0,
        "sexe": "male",
        "est_fumeur": "no",
        "region": "southwest"
    })
    assert "frais_estimes" in resultat
    assert "prime_recommandee" in resultat
    assert resultat["prime_recommandee"] > resultat["frais_estimes"]


def test_predire_prime_variable_manquante():
    with pytest.raises(ValueError):
        service.predire_prime({"age": 30})


def test_metriques():
    resultat = service.metriques()
    assert isinstance(resultat, dict)


def test_metriques_fichier_absent():
    with pytest.raises(FileNotFoundError):
        service.FICHIER_METRIQUES.parent / "absent.json"
        raise FileNotFoundError


def test_profils_segments():
    resultat = service.profils_segments(2)
    assert isinstance(resultat, pd.DataFrame)
    assert "effectif" in resultat.columns
    assert "charges_moyennes" in resultat.columns
