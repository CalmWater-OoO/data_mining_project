import runpy
import pytest
from backend import train


def test_main():
    resultat = train.main()
    assert isinstance(resultat, dict)
    assert resultat["nb_demandes"] > 0
    assert "mae_cv_moyenne" in resultat
    assert "mae_cv_ecart_type" in resultat
    assert "r2_modele" in resultat

def test_execution_main():
    runpy.run_module("backend.train", run_name="__main__")