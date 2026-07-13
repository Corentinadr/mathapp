import streamlit as st

# Source unique de vérité pour la navigation : (slug URL, glyphe, titre, sous-titre, domaine)
PAGES = [
    ("Équation_2nd_degré", "x²", "Équation du 2nd degré", "Discriminant, nature et calcul des racines", "Algèbre"),
    ("Dérivée", "f′(x)", "Dérivée", "Règles de dérivation, ordres supérieurs", "Analyse"),
    ("Primitive", "F(x)", "Primitive", "Antidérivée et constante d'intégration", "Analyse"),
    ("Intégrale_définie", "∫", "Intégrale définie", "Théorème fondamental, F(b) − F(a)", "Analyse"),
    ("Limite", "lim", "Limite", "Substitution directe, formes indéterminées", "Analyse"),
    ("Développement_limité", "o(xⁿ)", "Développement limité", "Formule de Taylor-Young, reste", "Analyse"),
]

_CSS = """
<style>
/* ---- Chrome Streamlit masqué : le header custom prend le relais ---- */
header[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
[data-testid="stMainBlockContainer"], .block-container { padding-top: 4.8rem !important; }

/* ---- Header fixe ---- */
.ma-header {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    background: var(--ma-header-bg);
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    border-bottom: 1px solid var(--ma-border);
}
.ma-header-inner {
    max-width: 1120px; margin: 0 auto; padding: 0 66px 0 24px; height: 56px;
    display: flex; align-items: center; justify-content: space-between;
}
.ma-logo {
    display: inline-flex; align-items: center; gap: 9px;
    font-size: 15.5px; font-weight: 700; letter-spacing: -0.02em;
    color: var(--ma-text-1) !important; text-decoration: none !important;
}
.ma-logo-glyph {
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px; border-radius: 8px;
    background: var(--ma-accent); color: #fff;
    font-family: Georgia, 'Times New Roman', serif; font-size: 15px;
    transition: transform 200ms ease;
}
.ma-logo:hover .ma-logo-glyph { transform: rotate(-8deg) scale(1.08); }

.ma-nav { display: flex; align-items: center; gap: 2px; }
.ma-nav-link {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 7px 12px; border-radius: 8px;
    font-size: 14px; font-weight: 500;
    color: var(--ma-nav-fg) !important; text-decoration: none !important;
    cursor: pointer; transition: all 150ms ease;
}
.ma-nav-link:hover { color: var(--ma-text-1) !important; background: var(--ma-nav-hover); }

/* ---- Menu déroulant ---- */
.ma-dd { position: relative; }
.ma-chev { transition: transform 200ms ease; }
.ma-dd:hover .ma-chev { transform: rotate(180deg); }
.ma-dd-panel {
    position: absolute; top: 100%; left: 50%;
    transform: translate(-50%, 6px);
    padding-top: 10px;
    opacity: 0; visibility: hidden; pointer-events: none;
    transition: all 200ms cubic-bezier(0.2, 0.8, 0.3, 1);
}
.ma-dd:hover .ma-dd-panel {
    opacity: 1; visibility: visible; pointer-events: auto;
    transform: translate(-50%, 0);
}
.ma-dd-inner {
    min-width: 330px; background: var(--ma-surface);
    border: 1px solid var(--ma-border); border-radius: 14px;
    box-shadow: var(--ma-shadow-pop);
    padding: 8px;
}
.ma-dd-item {
    display: flex; align-items: center; gap: 12px;
    padding: 9px 12px; border-radius: 10px;
    text-decoration: none !important;
    transition: background 150ms ease;
}
.ma-dd-item:hover { background: var(--ma-surface-hover); }
.ma-dd-glyph {
    flex: none; min-width: 40px; height: 36px; padding: 0 7px;
    border-radius: 10px; background: var(--ma-accent-soft); color: var(--ma-accent-text);
    display: inline-flex; align-items: center; justify-content: center;
    font-family: Georgia, 'Times New Roman', serif; font-style: italic; font-size: 13px;
    transition: all 200ms ease;
}
.ma-dd-item:hover .ma-dd-glyph { background: var(--ma-accent); color: #fff; transform: scale(1.06); }
.ma-dd-titre { display: block; font-size: 14px; font-weight: 600; color: var(--ma-text-1); letter-spacing: -0.01em; }
.ma-dd-sous { display: block; font-size: 12px; color: var(--ma-text-3); margin-top: 1px; }

@media (prefers-reduced-motion: reduce) {
    .ma-header *, .ma-header { transition: none !important; }
}
</style>
"""


def _liens_dropdown() -> str:
    items = []
    for slug, glyphe, titre, sous_titre, _ in PAGES:
        items.append(
            f'<a class="ma-dd-item" href="/{slug}" target="_self">'
            f'<span class="ma-dd-glyph">{glyphe}</span>'
            f'<span><span class="ma-dd-titre">{titre}</span>'
            f'<span class="ma-dd-sous">{sous_titre}</span></span></a>'
        )
    return "".join(items)


def afficher_entete() -> None:
    """Header fixe avec menu déroulant. À appeler sur chaque page, après set_page_config."""
    chevron = (
        '<svg class="ma-chev" width="11" height="11" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>'
    )
    header = (
        '<div class="ma-header"><div class="ma-header-inner">'
        '<a class="ma-logo" href="/" target="_self"><span class="ma-logo-glyph">∫</span>MathApp</a>'
        '<nav class="ma-nav">'
        '<a class="ma-nav-link" href="/" target="_self">Accueil</a>'
        f'<div class="ma-dd"><span class="ma-nav-link">Exercices{chevron}</span>'
        f'<div class="ma-dd-panel"><div class="ma-dd-inner">{_liens_dropdown()}</div></div></div>'
        '<a class="ma-nav-link" href="/Entraînement" target="_self">Entraînement</a>'
        '<a class="ma-nav-link" href="/Formulaire" target="_self">Formulaire</a>'
        '</nav></div></div>'
    )
    st.markdown(_CSS + header, unsafe_allow_html=True)
