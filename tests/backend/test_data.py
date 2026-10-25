import sqlite3
import pandas as pd
import pytest
from backend.data import charger_brut_dans_sqlite, lire_table_analyse

@pytest.fixture
def base_de_test(tmp_path):
    fichier_csv = tmp_path / "insurance_test.csv"
    fichier_db = tmp_path / "assurance_test.db"
    
    # On crée 3 lignes dont un doublon parfait
    df_brut = pd.DataFrame({
        "age": [19, 18, 19],
        "sex": ["female", "male", "female"],
        "bmi": [27.9, 33.77, 27.9],
        "children": [0, 1, 0],
        "smoker": ["yes", "no", "yes"],
        "region": ["southwest", "southeast", "southwest"],
        "charges": [16884.92, 1725.55, 16884.92]
    })
    df_brut.to_csv(fichier_csv, index=False)
    
    return fichier_csv, fichier_db

def test_charger_brut_dans_sqlite(base_de_test):
    fichier_csv, fichier_db = base_de_test
    nb_lignes = charger_brut_dans_sqlite(fichier=fichier_csv, base=fichier_db)
    
    assert nb_lignes == 3
    assert fichier_db.exists()
    
    with sqlite3.connect(fichier_db) as con:
        df_verif = pd.read_sql("SELECT * FROM assurance", con)
        assert len(df_verif) == 3
        assert "id_assure" in df_verif.columns

def test_lire_table_analyse(base_de_test):
    fichier_csv, fichier_db = base_de_test
    # 1. On charge nos données de test
    charger_brut_dans_sqlite(fichier=fichier_csv, base=fichier_db)
    
    # On exécute la vraie fonction 
    df_analyse = lire_table_analyse(base=fichier_db)
    
    # Verifications : le GROUP BY du SQL doit avoir retiré le doublon 
    assert len(df_analyse) == 2
    assert "imc" in df_analyse.columns
    assert "est_fumeur" in df_analyse.columns
    assert df_analyse["sexe"].iloc[0] in ["homme", "femme"]
    assert df_analyse["est_fumeur"].isin([0, 1]).all()


def test_charger_brut_fichier_introuvable(tmp_path):
    """Vérifie que FileNotFoundError est levé si le CSV brut n'existe pas."""
    faux_fichier = tmp_path / "inexistant.csv"
    fausse_base = tmp_path / "assurance.db"
    
    with pytest.raises(FileNotFoundError):
        charger_brut_dans_sqlite(fichier=faux_fichier, base=fausse_base)

def test_lire_table_analyse_base_introuvable(tmp_path):
    """Vérifie que FileNotFoundError est levé si la base SQLite n'existe pas encore."""
    fausse_base = tmp_path / "base_inexistante.db"
    
    with pytest.raises(FileNotFoundError):
        lire_table_analyse(base=fausse_base)    