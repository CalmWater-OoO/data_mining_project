
import json
import pandas as pd
import pytest
from backend import service


def test_modele_introuvable(monkeypatch, tmp_path):
    monkeypatch.setattr(service, "FICHIER_MODELE", tmp_path / "absent.joblib")
    with pytest.raises(FileNotFoundError):
        service._modele()


def test_lister_assures(monkeypatch):
    df = pd.DataFrame({"age": [20]})
    monkeypatch.setattr(service, "lire_table_analyse", lambda: df)
    pd.testing.assert_frame_equal(service.lister_assures(), df)


def test_predire_prime(monkeypatch):
    class Modele:
        def predict(self, df):
            return [1000.0]

    monkeypatch.setattr(service, "VARIABLES", ["age"])
    monkeypatch.setattr(service, "_modele", lambda: Modele())
    monkeypatch.setattr(service, "regle_tarifaire", lambda x: x * 1.2)

    resultat = service.predire_prime({"age": 30})
    assert resultat == {
        "frais_estimes": 1000.0,
        "prime_recommandee": 1200.0,
    }


def test_predire_prime_variable_manquante(monkeypatch):
    monkeypatch.setattr(service, "VARIABLES", ["age", "bmi"])
    with pytest.raises(ValueError, match="Variables manquantes"):
        service.predire_prime({"age": 30})


def test_metriques(monkeypatch, tmp_path):
    fichier = tmp_path / "metriques.json"
    fichier.write_text('{"r2": 0.9}', encoding="utf-8")
    monkeypatch.setattr(service, "FICHIER_METRIQUES", fichier)
    assert service.metriques() == {"r2": 0.9}


def test_metriques_fichier_absent(monkeypatch, tmp_path):
    monkeypatch.setattr(service, "FICHIER_METRIQUES", tmp_path / "absent.json")
    with pytest.raises(FileNotFoundError):
        service.metriques()


def test_profils_segments(monkeypatch):
    df = pd.DataFrame({
        "age": [20, 40],
        "charges": [1000.0, 3000.0],
        "segment": [0, 1],
    })
    monkeypatch.setattr(service, "VARIABLES_SEGMENTATION", ["age"])
    monkeypatch.setattr(service, "lister_assures", lambda: df)
    monkeypatch.setattr(service, "segmenter", lambda table, k: table)

    resultat = service.profils_segments(2)
    assert list(resultat.columns) == [
        "effectif", "age", "charges_moyennes"
    ]
    assert resultat.loc[0, "effectif"] == 1
    assert resultat.loc[1, "charges_moyennes"] == 3000.0
