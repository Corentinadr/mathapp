import random

import sympy as sp
import streamlit as st

from core.execution import CalculTropLong, calculer
from core.generateur import TYPES, generer, resoudre
from ui.config import configurer_page
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Entraînement")

st.title("Entraînement")
st.markdown("Un exercice tiré au hasard : cherche sur papier, puis révèle la correction détaillée.")

_LIBELLES = {
    "Au hasard": None,
    "Équation du 2nd degré": "equation",
    "Dérivée": "derivee",
    "Primitive": "primitive",
    "Limite": "limite",
    "Développement limité": "dl",
}

choix = st.selectbox("Type d'exercice", list(_LIBELLES))
type_choisi = _LIBELLES[choix]

nouveau = st.button("Nouvel exercice", type="primary")
type_a_change = (
    "exo" in st.session_state
    and type_choisi is not None
    and st.session_state.exo["type"] != type_choisi
)

if nouveau or type_a_change or "exo" not in st.session_state:
    st.session_state.exo = generer(type_choisi or random.choice(TYPES))
    st.session_state.correction_visible = False

exo = st.session_state.exo

st.markdown(f"**Énoncé** — {exo['consigne']}")
with st.container(border=True):
    st.latex(exo["latex"])

if st.button("Voir la correction"):
    st.session_state.correction_visible = True

if st.session_state.get("correction_visible"):
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(resoudre, exo)
    except CalculTropLong as e:
        st.error(str(e))
    else:
        st.divider()
        afficher_etapes(solution)
        if exo["type"] == "equation":
            racines = solution.resultat
            if len(racines) == 1:
                afficher_resultat("x = " + sp.latex(racines[0]))
            else:
                afficher_resultat(
                    r"x_1 = " + sp.latex(racines[0]) + r" \quad,\quad x_2 = " + sp.latex(racines[1])
                )
        elif exo["type"] == "primitive":
            afficher_resultat("F(x) = " + sp.latex(solution.resultat))
        elif exo["type"] == "limite":
            afficher_resultat("L = " + sp.latex(solution.resultat))
        else:
            afficher_resultat(sp.latex(solution.resultat))
