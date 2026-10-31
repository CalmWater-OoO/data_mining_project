import pandas as pd
from backend.model import creer_pipeline, regle_tarifaire, calculer_mae, segmenter

def test_creer_pipeline():
    assert creer_pipeline() is not None

def test_regle_tarifaire():
    assert regle_tarifaire(1000) == 1100.0

def test_calculer_mae():
    assert calculer_mae([100, 200], [110, 180]) == 15.0

def test_segmenter():
    df = pd.DataFrame({"age": [20, 30, 50, 60], "imc": [20, 25, 30, 35], "charges": [1000, 2000, 5000, 6000]})
    resultat = segmenter(df, 2)
    assert "segment" in resultat.columns
    assert resultat["segment"].nunique() == 2
    assert len(resultat) == 4
