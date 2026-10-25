# tests/test_sql.py
import pytest
from backend.config import REQUETE_ANALYSE

def test_fichier_sql_existe():
    assert REQUETE_ANALYSE.exists(), "Le fichier table_analyse.sql est introuvable."

def test_contenu_requete_sql():
    contenu = REQUETE_ANALYSE.read_text(encoding="utf-8").upper()
    
    assert "SELECT" in contenu
    assert "FROM ASSURANCE" in contenu
    assert "CASE WHEN" in contenu, "La requête doit contenir des conditions de transformation"
    assert "GROUP BY" in contenu, "La requête doit traiter les doublons via un GROUP BY"