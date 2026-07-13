import sympy as sp
import streamlit as st

from solvers.algebre.equations import resoudre_second_degre
from core.execution import CalculTropLong, calculer
from ui.config import configurer_page
from ui.graphes import tracer
from ui.historique import ajouter, choisir
from ui.rendu import afficher_etapes, afficher_resultat

sombre = configurer_page("Équation du 2nd degré")

st.title("Équation du 2nd degré")
st.markdown("Résout $ax^2 + bx + c = 0$ par la méthode du discriminant, avec explications à chaque étape.")

col_a, col_b, col_c = st.columns(3)
with col_a:
    a = st.number_input("a", value=1.0, step=1.0)
with col_b:
    b = st.number_input("b", value=-3.0, step=1.0)
with col_c:
    c = st.number_input("c", value=2.0, step=1.0)

lancer = st.button("Résoudre", type="primary")
rejeu = choisir("equation")

if lancer or rejeu:
    if rejeu:
        a, b, c = rejeu["a"], rejeu["b"], rejeu["c"]
    try:
        with st.spinner("Calcul en cours…"):
            solution = calculer(resoudre_second_degre, a, b, c)
    except (ValueError, CalculTropLong) as e:
        st.error(str(e))
    else:
        ajouter("equation", f"a={a:g}, b={b:g}, c={c:g}", {"a": a, "b": b, "c": c})
        afficher_etapes(solution)

        if len(solution.resultat) == 1:
            afficher_resultat("x = " + sp.latex(solution.resultat[0]))
        else:
            afficher_resultat(
                r"x_1 = " + sp.latex(solution.resultat[0])
                + r" \quad,\quad x_2 = " + sp.latex(solution.resultat[1])
            )
        try:
            x_sym = sp.Symbol("x")
            trinome = sp.nsimplify(a) * x_sym**2 + sp.nsimplify(b) * x_sym + sp.nsimplify(c)
            racines = [float(r) for r in solution.resultat if sp.im(r) == 0]
            if racines:
                centre = sum(racines) / len(racines)
                demi = max(max(abs(r - centre) for r in racines) * 2.0, 3.0)
            else:
                centre = -b / (2 * a)
                demi = 3.0
            tracer(
                [(trinome, "ax² + bx + c")],
                x_sym, centre - demi, centre + demi, sombre,
                points=[(r, 0.0) for r in racines] or None,
                titre="Visualisation — parabole et racines",
            )
        except Exception:
            pass
