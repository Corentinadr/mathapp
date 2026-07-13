import sympy as sp
import streamlit as st

from core.types import Solution


def afficher_etapes(solution: Solution) -> None:
    """Affiche les étapes d'une Solution : titre, formule LaTeX, explication, séparateur."""
    st.subheader("Étapes")
    for etape in solution.etapes:
        st.markdown(f"**{etape.title}**")
        st.latex(sp.latex(etape.expression))
        if etape.explication:
            st.markdown(etape.explication)
        st.divider()


def afficher_resultat(latex: str) -> None:
    """Affiche le résultat final, mis en valeur dans une carte, avec le LaTeX copiable."""
    st.subheader("Résultat")
    with st.container(border=True):
        st.latex(latex)
    with st.expander("Copier le LaTeX"):
        st.code(latex, language="latex")
