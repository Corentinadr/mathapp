import sympy as sp
import streamlit as st

from solvers.analyse.limites import calculer_limite
from core.execution import CalculTropLong, calculer
from core.parser import parse
from core.suggestions import LIMITE, LIMITE_POINTS
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Limite")

st.title("Limite")
st.markdown(r"Calcule $\lim_{x \to a} f(x)$ en détectant les formes indéterminées.")

expression = st.selectbox(
    "Fonction f(x)",
    options=LIMITE,
    accept_new_options=True,
    help="Choisis un exemple ou tape ta propre fonction.",
)

col_p, col_v, col_d = st.columns(3)
with col_p:
    point = st.selectbox(
        "Point a",
        options=LIMITE_POINTS,
        accept_new_options=True,
        help="oo = +∞, -oo = −∞. Tape n'importe quelle valeur.",
    )
with col_v:
    variable = st.text_input("Variable", value="x")
with col_d:
    direction = st.selectbox("Direction", ["deux côtés", "à gauche", "à droite"])

lancer = st.button("Calculer la limite", type="primary")
rejeu = choisir("limite")

if lancer or rejeu:
    if rejeu:
        expression, point, variable, direction = (
            rejeu["expression"], rejeu["point"], rejeu["variable"], rejeu["direction"]
        )
    if not expression or not point:
        st.warning("Choisis ou saisis une fonction et un point d'abord.")
        st.stop()
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(calculer_limite, expression, point, variable=variable, direction=direction)
    except CalculTropLong as e:
        st.error(str(e))
    except (ValueError, SyntaxError, TypeError) as e:
        st.error(f"Impossible d'interpréter l'expression : {e}")
    else:
        etiquette = f"{expression} en {point}" + ("" if direction == "deux côtés" else f" ({direction})")
        ajouter(
            "limite",
            etiquette,
            {"expression": expression, "point": point, "variable": variable, "direction": direction},
        )
        afficher_etapes(solution)
        afficher_resultat("L = " + sp.latex(solution.resultat))
        try:
            a_sym = parse(str(point))
            if a_sym == sp.oo:
                x_min, x_max = 1.0, 60.0
            elif a_sym == -sp.oo:
                x_min, x_max = -60.0, -1.0
            else:
                centre = float(a_sym)
                x_min, x_max = centre - 4.0, centre + 4.0
            marqueurs = None
            if a_sym.is_finite and solution.resultat.is_finite:
                marqueurs = [(float(a_sym), float(solution.resultat))]
            tracer(
                [(parse(expression), "f")],
                sp.Symbol(variable), x_min, x_max, sombre,
                points=marqueurs,
                titre="Visualisation — comportement autour du point",
            )
        except Exception:
            pass
