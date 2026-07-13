import sympy as sp
import streamlit as st

from solvers.analyse.primitives import primitiver
from core.execution import CalculTropLong, calculer
from core.parser import parse
from core.suggestions import PRIMITIVE
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Primitive")

st.title("Primitive")
st.markdown("Calcule une primitive $F(x)$ telle que $F'(x) = f(x)$, avec explications des techniques utilisées.")

expression = st.selectbox(
    "Fonction f(x)",
    options=PRIMITIVE,
    accept_new_options=True,
    help="Choisis un exemple ou tape ta propre fonction. Utilise ^ pour les puissances.",
)

variable = st.text_input("Variable", value="x")

lancer = st.button("Calculer la primitive", type="primary")
rejeu = choisir("primitive")

if lancer or rejeu:
    if rejeu:
        expression, variable = rejeu["expression"], rejeu["variable"]
    if not expression:
        st.warning("Choisis ou saisis une fonction d'abord.")
        st.stop()
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(primitiver, expression, variable=variable)
    except CalculTropLong as e:
        st.error(str(e))
    except (ValueError, SyntaxError, TypeError) as e:
        st.error(f"Impossible d'interpréter l'expression : {e}")
    else:
        ajouter("primitive", expression, {"expression": expression, "variable": variable})
        afficher_etapes(solution)
        afficher_resultat("F(" + variable + ") = " + sp.latex(solution.resultat))
        try:
            F_sans_C = solution.resultat.subs(sp.Symbol("C"), 0)
            tracer(
                [(parse(expression), "f"), (F_sans_C, "F (avec C = 0)")],
                sp.Symbol(variable), -5, 5, sombre,
                titre="Visualisation — f et une primitive",
            )
        except Exception:
            pass
