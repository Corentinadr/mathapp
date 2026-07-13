import streamlit as st

# Palette custom (header, accueil, cartes) — les widgets Streamlit suivent
# [theme.light]/[theme.dark] de config.toml ; ces variables suivent le MÊME
# thème résolu, transmis par configurer_page (st.context.theme.type).

_VARS_CLAIR = """
:root {
    --ma-text-1: #171717;
    --ma-text-2: #525252;
    --ma-text-3: #737373;
    --ma-text-4: #A3A3A3;
    --ma-surface: #FFFFFF;
    --ma-surface-hover: #F5F5F7;
    --ma-border: #EAEAEA;
    --ma-border-hover: #D6D9F8;
    --ma-accent: #4F46E5;
    --ma-accent-text: #4F46E5;
    --ma-accent-soft: #EEF0FF;
    --ma-accent-border: #E0E3FC;
    --ma-header-bg: rgba(250, 250, 250, 0.85);
    --ma-nav-fg: #525252;
    --ma-nav-hover: #EEEEEE;
    --ma-btn-bg: #171717;
    --ma-btn-fg: #FFFFFF;
    --ma-btn-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
    --ma-ghost-border: #E0E0E0;
    --ma-ghost-hover-bg: #F0F0F0;
    --ma-ghost-hover-border: #D4D4D4;
    --ma-tag-fg: #737373;
    --ma-tag-bg: #F5F5F5;
    --ma-tag-border: #EAEAEA;
    --ma-shadow-card: 0 1px 3px rgba(0, 0, 0, 0.04);
    --ma-shadow-card-hover: 0 2px 10px rgba(0, 0, 0, 0.06);
    --ma-shadow-pop: 0 12px 32px rgba(0, 0, 0, 0.08);
    --ma-shadow-hover: 0 10px 28px rgba(79, 70, 229, 0.09);
    --ma-glow: 0 4px 14px rgba(79, 70, 229, 0.15);
}
"""

_VARS_SOMBRE = """
:root {
    --ma-text-1: #F2F2F2;
    --ma-text-2: #A9A9AE;
    --ma-text-3: #9A9A9E;
    --ma-text-4: #6E6E72;
    --ma-surface: #161619;
    --ma-surface-hover: #212124;
    --ma-border: #26262A;
    --ma-border-hover: #3B3E8F;
    --ma-accent: #6366F1;
    --ma-accent-text: #8B8FF5;
    --ma-accent-soft: rgba(99, 102, 241, 0.16);
    --ma-accent-border: rgba(99, 102, 241, 0.35);
    --ma-header-bg: rgba(14, 14, 16, 0.82);
    --ma-nav-fg: #A3A3A8;
    --ma-nav-hover: #232326;
    --ma-btn-bg: #EDEDED;
    --ma-btn-fg: #111111;
    --ma-btn-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
    --ma-ghost-border: #333338;
    --ma-ghost-hover-bg: #1E1E22;
    --ma-ghost-hover-border: #3F3F46;
    --ma-tag-fg: #9A9A9E;
    --ma-tag-bg: #1E1E22;
    --ma-tag-border: #2C2C30;
    --ma-shadow-card: 0 1px 3px rgba(0, 0, 0, 0.3);
    --ma-shadow-card-hover: 0 2px 10px rgba(0, 0, 0, 0.4);
    --ma-shadow-pop: 0 12px 32px rgba(0, 0, 0, 0.5);
    --ma-shadow-hover: 0 10px 28px rgba(0, 0, 0, 0.45);
    --ma-glow: 0 4px 14px rgba(99, 102, 241, 0.25);
}
"""

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Titres : graisse marquée, interlettrage resserré */
h1, h2, h3 {
    font-weight: 650 !important;
    letter-spacing: -0.02em !important;
}

/* Corps de texte : lisibilité */
.stMarkdown p, .stMarkdown li {
    line-height: 1.6;
}

/* Boutons : transition douce, hover discret */
.stButton > button {
    font-weight: 500;
    transition: all 200ms ease;
}
.stButton > button:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
}

/* Cartes (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--ma-surface);
    border-radius: 16px;
    box-shadow: var(--ma-shadow-card);
    transition: box-shadow 200ms ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: var(--ma-shadow-card-hover);
}

/* Liens de navigation entre pages */
[data-testid="stPageLink"] a {
    border-radius: 10px;
    transition: background 150ms ease;
    font-weight: 500;
}

/* Séparateurs discrets */
hr {
    border-color: var(--ma-border) !important;
}

/* Masquer le bouton Deploy (usage local) et les ancres de titres */
.stDeployButton {
    display: none;
}
[data-testid="stHeaderActionElements"] {
    display: none;
}

/* Bouton bascule clair/sombre : iframe fixée en haut à droite du header */
.st-key-bascule_theme {
    height: 0 !important;
    min-height: 0 !important;
    margin: 0;
    padding: 0;
}
.st-key-bascule_theme iframe {
    position: fixed;
    top: 10px;
    right: max(20px, calc((100vw - 1120px) / 2 + 20px));
    width: 38px !important;
    height: 38px !important;
    z-index: 1001;
    border: none;
    background: transparent;
}

/* Barre de recherche (accueil) */
.st-key-recherche {
    max-width: 620px;
    margin: 0 auto;
}
.st-key-recherche iframe {
    width: 100% !important;
    border: none;
    background: transparent;
}
"""


def appliquer_style(sombre: bool = False) -> None:
    """Injecte les variables de palette (selon le thème résolu) + le CSS global."""
    variables = _VARS_SOMBRE if sombre else _VARS_CLAIR
    st.markdown(f"<style>{variables}{_CSS}</style>", unsafe_allow_html=True)
