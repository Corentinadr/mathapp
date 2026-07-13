import sympy as sp
import streamlit as st

from solvers.analyse.dl import developpement_limite
from core.execution import CalculTropLong, calculer
from core.parser import parse
from core.suggestions import DL
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Développement limité")

st.title("Développement limité")
st.markdown(
    r"Calcule le DL (Taylor-Young) de $f$ autour d'un point à l'ordre choisi, "
    "en rappelant la formule appliquée."
)

expression = st.selectbox(
    "Fonction f(x)",
    options=DL,
    accept_new_options=True,
    help="Choisis un exemple ou tape ta propre fonction.",
)

col_p, col_o, col_v = st.columns(3)
with col_p:
    point = st.text_input("Point a", value="0", help="0 pour un DL en 0 (Maclaurin).")
with col_o:
    ordre = st.number_input("Ordre", value=5, min_value=1, max_value=20, step=1)
with col_v:
    variable = st.text_input("Variable", value="x")

lancer = st.button("Calculer le DL", type="primary")
rejeu = choisir("dl")

if lancer or rejeu:
    if rejeu:
        expression, point, ordre, variable = (
            rejeu["expression"], rejeu["point"], rejeu["ordre"], rejeu["variable"]
        )
    if not expression:
        st.warning("Choisis ou saisis une fonction d'abord.")
        st.stop()
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(
                developpement_limite, expression, point=point, ordre=int(ordre), variable=variable
            )
    except CalculTropLong as e:
        st.error(str(e))
    except (ValueError, SyntaxError, TypeError) as e:
        st.error(f"Impossible d'interpréter l'expression : {e}")
    else:
        ajouter(
            "dl",
            f"{expression} en {point}, ordre {int(ordre)}",
            {"expression": expression, "point": point, "ordre": int(ordre), "variable": variable},
        )
        afficher_etapes(solution)
        afficher_resultat("f(" + variable + ") = " + sp.latex(solution.resultat))
        try:
            polynome = solution.resultat.removeO()
            centre = float(parse(str(point)))
            tracer(
                [(parse(expression), "f"), (polynome, f"DL ordre {int(ordre)}")],
                sp.Symbol(variable), centre - 3.5, centre + 3.5, sombre,
                titre="Visualisation — f contre son polynôme de Taylor",
            )
        except Exception:
            pass
