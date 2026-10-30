"""Interface Streamlit pour la prédiction des charges d'assurance."""

import pandas as pd
import streamlit as st
from backend import service


# Configuration générale de l'application
st.set_page_config(
    page_title="Assurance : prédiction des charges",
    layout="wide",)
st.title("Prédiction des charges médicales")
st.caption("Application de démonstration utilisant une forêt aléatoire pour estimer les charges médicales des assurés.")


# Chargement des données
@st.cache_data
def charger_assures() -> pd.DataFrame:
    return service.lister_assures()


# Vérification de la disponibilité du modèle et des métriques
try:
    metriques = service.metriques()
except FileNotFoundError:
    st.error("Modèle ou métriques absents. Lancer d'abord : `python -m backend.train`")
    st.stop()



# Création des onglets
onglet_prediction, onglet_segments, onglet_modele = st.tabs(
    ["Estimer les charges","Segmentation des assurés","Évaluation du modèle",])


# ONGLET 1 : PRÉDICTION
with onglet_prediction:
    st.subheader("Estimation des frais médicaux")
    st.write("Cet espace permettra de sélectionner un assuré et d'estimer ses frais médicaux.")


# ONGLET 2 : SEGMENTATION
with onglet_segments:

    st.subheader("Segmentation des assurés")

    k = st.slider(
        "Nombre de segments",
        min_value=2,
        max_value=6,
        value=3,
    )

    try:
        profils = service.profils_segments(k)
        st.dataframe(profils, use_container_width=True)

    except (FileNotFoundError, KeyError) as erreur:
        st.error(f"Impossible de calculer les segments : {erreur}")


# ONGLET 3 : ÉVALUATION
with onglet_modele:

    st.subheader("Performances du modèle")

    colonne1, colonne2, colonne3 = st.columns(3)

    colonne1.metric(
        "R² sur le jeu de test",
        f"{metriques['r2_modele']:.3f}",
    )

    colonne2.metric(
        "MAE du modèle",
        f"{metriques['mae_modele']:.2f} $",
    )

    colonne3.metric(
        "MAE de référence",
        f"{metriques['mae_baseline']:.2f} $",
    )

    st.subheader("Importance des variables")

    importances = pd.Series(
        metriques["importance_permutation"],
        name="Importance",
    ).sort_values(ascending=False)

    st.bar_chart(importances)

    st.caption(
        "L'importance par permutation mesure la dégradation "
        "des performances lorsque les valeurs d'une variable "
        "sont mélangées. Une valeur élevée indique une variable "
        "utile aux prédictions du modèle."
    )