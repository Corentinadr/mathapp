import sympy as sp
import streamlit as st

from solvers.analyse.derivees import deriver
from core.execution import CalculTropLong, calculer
from core.parser import parse
from core.suggestions import DERIVEE
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Dérivée")

st.title("Dérivée")
st.markdown("Calcule $f'(x)$ (ou d'ordre supérieur) en rappelant les règles de dérivation utilisées.")

expression = st.selectbox(
    "Fonction f(x)",
    options=DERIVEE,
    accept_new_options=True,
    help="Choisis un exemple ou tape ta propre fonction. Utilise ^ pour les puissances.",
)

col_v, col_o = st.columns(2)
with col_v:
    variable = st.text_input("Variable", value="x")
with col_o:
    ordre = st.number_input("Ordre de dérivation", value=1, min_value=1, max_value=10, step=1)

lancer = st.button("Dériver", type="primary")
rejeu = choisir("derivee")

if lancer or rejeu:
    if rejeu:
        expression, variable, ordre = rejeu["expression"], rejeu["variable"], rejeu["ordre"]
    if not expression:
        st.warning("Choisis ou saisis une fonction d'abord.")
        st.stop()
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(deriver, expression, variable=variable, ordre=int(ordre))
    except CalculTropLong as e:
        st.error(str(e))
    except (ValueError, SyntaxError, TypeError) as e:
        st.error(f"Impossible d'interpréter l'expression : {e}")
    else:
        etiquette = expression if int(ordre) == 1 else f"{expression} — ordre {int(ordre)}"
        ajouter("derivee", etiquette, {"expression": expression, "variable": variable, "ordre": int(ordre)})
        afficher_etapes(solution)
        afficher_resultat(sp.latex(solution.resultat))
        try:
            tracer(
                [(parse(expression), "f"), (solution.resultat, "f" + "′" * int(ordre))],
                sp.Symbol(variable), -5, 5, sombre,
                titre="Visualisation — f et sa dérivée",
            )
        except Exception:
            pass
