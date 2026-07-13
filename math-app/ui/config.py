from pathlib import Path

import streamlit as st

from ui.bascule import afficher_bascule
from ui.entete import afficher_entete
from ui.style import appliquer_style

_FAVICON = str(Path(__file__).resolve().parent.parent / "assets" / "favicon.png")


def configurer_page(titre: str | None = None) -> bool:
    """Config commune : favicon logo ∫, style global, header fixe, bascule clair/sombre.

    `titre=None` → page d'accueil (layout large). Sinon page d'exercice (layout centré).
    À appeler en premier sur chaque page. Retourne True si le thème résolu est sombre.
    """
    st.set_page_config(
        page_title=f"{titre} — MathApp" if titre else "MathApp — résolveur expliqué",
        page_icon=_FAVICON,
        layout="centered" if titre else "wide",
        initial_sidebar_state="collapsed",
    )
    sombre = st.context.theme.type == "dark"
    appliquer_style(sombre)
    afficher_entete()
    with st.container(key="bascule_theme"):
        afficher_bascule(sombre)
    return sombre
