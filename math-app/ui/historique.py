from typing import Any

import streamlit as st

_CLE = "historique"
_MAX_ENTREES = 8


def ajouter(exercice: str, etiquette: str, params: dict[str, Any]) -> None:
    """Mémorise un calcul réussi (dédoublonné, plafonné, plus récent en premier)."""
    historiques = st.session_state.setdefault(_CLE, {})
    entrees = historiques.setdefault(exercice, [])
    entrees[:] = [e for e in entrees if e["etiquette"] != etiquette]
    entrees.insert(0, {"etiquette": etiquette, "params": params})
    del entrees[_MAX_ENTREES:]


def choisir(exercice: str) -> dict[str, Any] | None:
    """Affiche l'historique de l'exercice ; retourne les params à rejouer si clic, sinon None."""
    entrees = st.session_state.get(_CLE, {}).get(exercice, [])
    if not entrees:
        return None

    choix: dict[str, Any] | None = None
    with st.expander(f"Historique de la session ({len(entrees)})"):
        for i, entree in enumerate(entrees):
            if st.button(f"↻ {entree['etiquette']}", key=f"hist_{exercice}_{i}"):
                choix = entree["params"]
    return choix
