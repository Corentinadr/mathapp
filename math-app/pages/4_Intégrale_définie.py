import sympy as sp
import streamlit as st

from solvers.analyse.integrales import integrer
from core.execution import CalculTropLong, calculer
from core.parser import parse
from core.suggestions import INTEGRALE
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Intégrale définie")

st.title("Intégrale définie")
st.markdown(r"Calcule $\int_a^b f(x)\, dx$ via le théorème fondamental $F(b) - F(a)$.")

expression = st.selectbox(
    "Fonction f(x)",
    options=INTEGRALE,
    accept_new_options=True,
    help="Choisis un exemple ou tape ta propre fonction. Utilise ^ pour les puissances.",
)

col_a, col_b, col_v = st.columns(3)
with col_a:
    borne_inf = st.text_input("Borne inférieure a", value="0")
with col_b:
    borne_sup = st.text_input("Borne supérieure b", value="1")
with col_v:
    variable = st.text_input("Variable", value="x")

st.caption("Bornes acceptées : nombres (0, -1, 2.5), fractions (1/2), constantes (pi, E), infini (oo, -oo).")

lancer = st.button("Calculer l'intégrale", type="primary")
rejeu = choisir("integrale")

if lancer or rejeu:
    if rejeu:
        expression, borne_inf, borne_sup, variable = (
            rejeu["expression"], rejeu["borne_inf"], rejeu["borne_sup"], rejeu["variable"]
        )
    if not expression:
        st.warning("Choisis ou saisis une fonction d'abord.")
        st.stop()
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(integrer, expression, borne_inf, borne_sup, variable=variable)
    except CalculTropLong as e:
        st.error(str(e))
    except (ValueError, SyntaxError, TypeError) as e:
        st.error(f"Impossible d'interpréter l'expression : {e}")
    else:
        ajouter(
            "integrale",
            f"{expression} de {borne_inf} à {borne_sup}",
            {"expression": expression, "borne_inf": borne_inf, "borne_sup": borne_sup, "variable": variable},
        )
        afficher_etapes(solution)
        afficher_resultat("I = " + sp.latex(solution.resultat))
        try:
            a_val, b_val = parse(str(borne_inf)), parse(str(borne_sup))
            if a_val.is_finite and b_val.is_finite:
                a_f, b_f = float(a_val), float(b_val)
                largeur = max(abs(b_f - a_f), 1.0)
                tracer(
                    [(parse(expression), "f")],
                    sp.Symbol(variable), a_f - 0.6 * largeur, b_f + 0.6 * largeur, sombre,
                    remplissage=(a_f, b_f),
                    titre="Visualisation — aire sous la courbe",
                )
        except Exception:
            pass
