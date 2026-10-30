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
    table = charger_assures()
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

    # choix du profil
    type_profil = st.radio(
        "Quel type de profil souhaitez-vous utiliser ?",
        ["Nouvel assuré", "Assuré existant"],
        horizontal=True
    )

    #choix d'un assuré et pré-remplissage du formulaire avec les valeurs de l'assuré choisi ou les valeurs médianes pour un nouvel assuré
    profil_base = None
    if type_profil == "Assuré existant":
        client_id = st.selectbox("Sélectionner un assuré",
        table.index)
        profil_base = table.loc[client_id]
    if profil_base is None:
        age_defaut = int(table["age"].median())
        imc_defaut = float(table["imc"].median())
        enfants_defaut = int(table["enfants"].median())

        sexe_defaut = table["sexe"].mode().iloc[0]
        fumeur_defaut = table["est_fumeur"].mode().iloc[0]
        region_defaut = table["region"].mode().iloc[0]
    else:
        age_defaut = int(profil_base["age"])
        imc_defaut = float(profil_base["imc"])
        enfants_defaut = int(profil_base["enfants"])

        sexe_defaut = profil_base["sexe"]
        fumeur_defaut = profil_base["est_fumeur"]
        region_defaut = profil_base["region"]

    #création du formulaire
    colonne_saisie, colonne_resultat = st.columns(2)
    with colonne_saisie:
        st.markdown("Caractéristiques de l'assuré")
        age = st.slider(
            "Âge",
            int(table["age"].min()),
            int(table["age"].max()),
            age_defaut)
        
        imc = st.number_input(
            "IMC",
            min_value=float(table["imc"].min()),
            max_value=float(table["imc"].max()),
            value=imc_defaut,
            step=0.1)
        
        enfants = st.number_input(
            "Nombre d'enfants",
            int(table["enfants"].min()),
            int(table["enfants"].max()),
            enfants_defaut)
        
        options_sexe = sorted(table["sexe"].dropna().unique())
        sexe = st.selectbox(
            "Sexe",
            options_sexe,
            index=options_sexe.index(sexe_defaut))
        
        options_fumeur = sorted(table["est_fumeur"].dropna().unique())
        est_fumeur = st.selectbox(
            "Fumeur",
            options_fumeur,
            index=options_fumeur.index(fumeur_defaut),
            format_func=lambda x: "Yes" if x == 1 else "No")
        
        options_region = sorted(table["region"].dropna().unique())
        region = st.selectbox(
            "Région",
            options_region,
            index=options_region.index(region_defaut))

        calculer = st.button("Estimer les charges")

    #appel du modèle
        if calculer:
            demande = {
                "age": age,
                "imc": imc,
                "enfants": enfants,
                "sexe": sexe,
                "est_fumeur": est_fumeur,
                "region": region
            }
            
            resultat = service.predire_prime(demande)
        
            with colonne_resultat:
                st.markdown("Résultats de la prédiction")
                st.metric(
                    "Frais médicaux estimés",
                    f"{resultat['frais_estimes']:,.2f} $"
                )
                st.metric(
                    "Prime recommandée",
                    f"{resultat['prime_recommandee']:,.2f} $"
                )
                st.caption("La prime recommandée correspond aux frais estimés augmentés d'une marge de sécurité de 10 %.")



# ONGLET 2 : SEGMENTATION
with onglet_segments:

    st.subheader("Segmentation des assurés")
    st.write("Cette analyse regroupe les assurés selon leur âge, leur IMC et leurs charges médicales, afin d'identifier et regrouper des profils similaires.")
    st.metric("Nombre d'assurés analysés", len(table))
    
    k = st.slider(
        "Nombre de segments",
        min_value=2,
        max_value=6,
        value=3,
    )

    try:
        profils = service.profils_segments(k)
        st.subheader("Profil moyen de chaque segment")
        st.dataframe(profils, use_container_width=True)
        st.subheader("Répartition des assurés par segment")
        st.bar_chart(profils["effectif"])
        st.subheader("Charges médicales moyennes par segment")
        st.bar_chart(profils["charges_moyennes"])

    except (FileNotFoundError, KeyError) as erreur:
        st.error(f"Impossible de calculer les segments : {erreur}")


# ONGLET 3 : ÉVALUATION
with onglet_modele:

    st.subheader("Performances du modèle")
    st.write("Cet onglet permet d'évaluer la qualité des prédictions du modèle et d'identifier les variables qui contribuent le plus à ses estimations.")
    
    colonne1, colonne2, colonne3 = st.columns(3)
    with colonne1 : 
        st.metric(
            "R² sur le jeu de test",
            f"{metriques['r2_modele']:.3f}",)
        st.caption(
            "Le R² mesure la capacité du modèle à expliquer les variations des charges médicales. Plus il est proche de 1, meilleur est le modèle.")

    with colonne2 :
        st.metric(
            "MAE du modèle",
            f"{metriques['mae_modele']:.2f} $",)
        st.caption(
            "La MAE (erreur absolue moyenne) représente l'écart moyen entre les charges réelles et les charges prédites. Plus elle est faible, plus les prédictions sont précises.")

    with colonne3 : 
        st.metric(
            "MAE de référence",
            f"{metriques['mae_baseline']:.2f} $",)
        st.caption(
            "La MAE de référence correspond à l'erreur obtenue avec un modèle de comparaison, qui permet d'évaluer l'intérêt de notre modèle.")

    # Comparaison des performances
    mae_modele = metriques["mae_modele"]
    mae_baseline = metriques["mae_baseline"]

    st.subheader("Comparaison avec le modèle de référence")
    if mae_modele < mae_baseline:
        st.success(
            "Le modèle améliore les prédictions par rapport au modèle de référence.")
    elif mae_modele > mae_baseline:
        st.warning(
            "Le modèle présente une erreur plus élevée que le modèle de référence.")
    else:
        st.info(
            "Le modèle obtient les mêmes performances que le modèle de référence.")

    
    st.subheader("Importance des variables")
    importances = pd.Series(
        metriques["importance_permutation"],
        name="Importance",
    ).sort_values(ascending=False)

    st.bar_chart(importances)

    st.caption(
        "Une valeur élevée indique que la variable joue un rôle important "
        "dans la qualité des prédictions du modèle. Cette importance ne "
        "traduit toutefois pas nécessairement un lien de causalité avec "
        "le montant des charges médicales.")