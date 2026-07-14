import streamlit as st

from ui.config import configurer_page
from ui.entete import PAGES
from ui.recherche import afficher_recherche

sombre = configurer_page()

_CSS_ACCUEIL = """
<style>
.ma-home { max-width: 1120px; margin: 0 auto; }

@keyframes maUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---- Hero ---- */
.ma-hero { text-align: center; padding: 34px 0 6px; animation: maUp 500ms ease both; }
.ma-eyebrow {
    display: inline-block; font-size: 12.5px; font-weight: 600;
    color: var(--ma-accent-text); background: var(--ma-accent-soft);
    border: 1px solid var(--ma-accent-border);
    padding: 5px 14px; border-radius: 999px; margin-bottom: 20px;
    transition: all 200ms ease;
}
.ma-eyebrow:hover { transform: scale(1.04); box-shadow: var(--ma-glow); }
.ma-h1 {
    font-size: 50px; line-height: 1.1; font-weight: 700;
    letter-spacing: -0.03em; color: var(--ma-text-1); margin: 0 0 16px;
}
.ma-h1 .ma-acc { color: var(--ma-accent-text); }
.ma-sub {
    font-size: 16.5px; color: var(--ma-text-2); line-height: 1.6;
    max-width: 580px; margin: 0 auto 26px !important;
}
.ma-cta { display: flex; gap: 12px; justify-content: center; }
.ma-btn-primary, .ma-btn-ghost {
    padding: 11px 24px; border-radius: 999px;
    font-size: 14.5px; font-weight: 600;
    text-decoration: none !important; transition: all 200ms ease;
}
.ma-btn-primary { background: var(--ma-btn-bg); color: var(--ma-btn-fg) !important; border: 1px solid var(--ma-btn-bg); }
.ma-btn-primary:hover { transform: translateY(-2px); box-shadow: var(--ma-btn-shadow); }
.ma-btn-ghost { background: transparent; color: var(--ma-text-1) !important; border: 1px solid var(--ma-ghost-border); }
.ma-btn-ghost:hover { background: var(--ma-ghost-hover-bg); border-color: var(--ma-ghost-hover-border); transform: translateY(-2px); }
.ma-hero-meta {
    display: flex; gap: 8px 22px; flex-wrap: wrap; justify-content: center;
    margin-top: 26px; font-size: 13px; color: var(--ma-text-3);
}
.ma-hero-meta span { transition: color 150ms ease; cursor: default; }
.ma-hero-meta span:hover { color: var(--ma-text-1); }

/* ---- Section ---- */
.ma-section { display: flex; align-items: baseline; gap: 12px; margin: 34px 0 16px; animation: maUp 500ms ease 150ms both; }
.ma-section h2 { font-size: 21px; font-weight: 650; letter-spacing: -0.02em; color: var(--ma-text-1); margin: 0; }
.ma-section span { font-size: 13.5px; color: var(--ma-text-3); }

/* ---- Grille d'exercices ---- */
.ma-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 980px) { .ma-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .ma-grid { grid-template-columns: 1fr; } }
.ma-card {
    display: flex; flex-direction: column;
    background: var(--ma-surface); border: 1px solid var(--ma-border); border-radius: 16px;
    padding: 20px 22px; text-decoration: none !important;
    transition: all 200ms ease;
    animation: maUp 500ms ease both;
    animation-delay: calc(var(--i) * 70ms + 200ms);
}
.ma-card:hover {
    transform: translateY(-3px);
    border-color: var(--ma-border-hover);
    box-shadow: var(--ma-shadow-hover);
}
.ma-card-head { display: flex; justify-content: space-between; align-items: flex-start; }
.ma-glyph {
    min-width: 44px; height: 40px; padding: 0 8px; border-radius: 12px;
    background: var(--ma-accent-soft); color: var(--ma-accent-text);
    display: inline-flex; align-items: center; justify-content: center;
    font-family: Georgia, 'Times New Roman', serif; font-style: italic; font-size: 15px;
    transition: all 200ms ease;
}
.ma-card:hover .ma-glyph { background: var(--ma-accent); color: #fff; transform: scale(1.07) rotate(-3deg); }
.ma-tag {
    font-size: 11px; font-weight: 600; color: var(--ma-tag-fg);
    background: var(--ma-tag-bg); border: 1px solid var(--ma-tag-border);
    padding: 3px 9px; border-radius: 999px;
}
.ma-card-titre { font-size: 16px; font-weight: 650; color: var(--ma-text-1); letter-spacing: -0.015em; margin-top: 12px; }
.ma-card-sous { font-size: 13.5px; color: var(--ma-text-3); line-height: 1.5; margin-top: 3px; }
.ma-card-go {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 13px; font-weight: 600; color: var(--ma-accent-text);
    margin-top: 12px; opacity: 0; transform: translateX(-5px);
    transition: all 200ms ease;
}
.ma-card:hover .ma-card-go { opacity: 1; transform: translateX(0); }

/* ---- Bannière formulaire ---- */
.ma-banner {
    display: flex; align-items: center; gap: 16px;
    margin-top: 16px; padding: 18px 24px;
    background: var(--ma-surface); border: 1px solid var(--ma-border); border-radius: 16px;
    text-decoration: none !important;
    transition: all 200ms ease;
    animation: maUp 500ms ease 650ms both;
}
.ma-banner:hover {
    transform: translateY(-2px);
    border-color: var(--ma-border-hover);
    box-shadow: var(--ma-shadow-hover);
}
.ma-banner-glyph {
    flex: none; width: 44px; height: 44px; border-radius: 12px;
    background: var(--ma-accent-soft); color: var(--ma-accent-text);
    display: flex; align-items: center; justify-content: center;
    transition: all 200ms ease;
}
.ma-banner:hover .ma-banner-glyph { background: var(--ma-accent); color: #fff; transform: scale(1.07); }
.ma-banner-titre { display: block; font-size: 15.5px; font-weight: 650; color: var(--ma-text-1); letter-spacing: -0.015em; }
.ma-banner-sous { display: block; font-size: 13.5px; color: var(--ma-text-3); margin-top: 2px; }
.ma-banner-arrow { margin-left: auto; color: var(--ma-text-4); transition: all 200ms ease; }
.ma-banner:hover .ma-banner-arrow { color: var(--ma-accent-text); transform: translateX(5px); }

.ma-foot { text-align: center; font-size: 12.5px; color: var(--ma-text-4); margin: 34px 0 6px; }

@media (prefers-reduced-motion: reduce) {
    .ma-home *, .ma-home { animation: none !important; transition: none !important; }
}
</style>
"""


def _carte(i: int, slug: str, glyphe: str, titre: str, sous_titre: str, domaine: str) -> str:
    fleche = (
        '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
    )
    return (
        f'<a class="ma-card" style="--i:{i}" href="/{slug}" target="_top">'
        f'<span class="ma-card-head"><span class="ma-glyph">{glyphe}</span>'
        f'<span class="ma-tag">{domaine}</span></span>'
        f'<span class="ma-card-titre">{titre}</span>'
        f'<span class="ma-card-sous">{sous_titre}</span>'
        f'<span class="ma-card-go">Résoudre {fleche}</span></a>'
    )


_LIVRE = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
    '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>'
)

_FLECHE_BANNER = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
)

_CIBLE = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
)

cartes = "".join(_carte(i, *page) for i, page in enumerate(PAGES))

hero = (
    _CSS_ACCUEIL
    + '<div class="ma-home">'
    + '<section class="ma-hero">'
    + '<span class="ma-eyebrow">Niveau supérieur · 6 modules · 100 % expliqué</span>'
    + '<h1 class="ma-h1">Résoudre, c\'est bien.<br><span class="ma-acc">Comprendre, c\'est mieux.</span></h1>'
    + '<p class="ma-sub">MathApp détaille chaque calcul : la méthode choisie, la formule appliquée '
    + 'et toutes les étapes intermédiaires, avec un rendu LaTeX soigné.</p>'
    + '<div class="ma-cta">'
    + '<a class="ma-btn-primary" href="/Dérivée" target="_top">Commencer un calcul</a>'
    + '<a class="ma-btn-ghost" href="/Formulaire" target="_top">Voir le formulaire</a>'
    + '</div>'
    + '<div class="ma-hero-meta"><span>Étapes expliquées</span><span>·</span>'
    + '<span>Formules usuelles intégrées</span><span>·</span><span>Moteur SymPy</span></div>'
    + '</section></div>'
)
st.markdown(hero, unsafe_allow_html=True)

with st.container(key="recherche"):
    afficher_recherche(sombre)

contenu = (
    '<div class="ma-home">'
    + '<div class="ma-section"><h2>Exercices</h2><span>Chaque module explique sa démarche pas à pas</span></div>'
    + f'<section class="ma-grid">{cartes}</section>'
    + '<a class="ma-banner" href="/Formulaire" target="_top">'
    + f'<span class="ma-banner-glyph">{_LIVRE}</span>'
    + '<span><span class="ma-banner-titre">Formulaire</span>'
    + '<span class="ma-banner-sous">Dérivées, primitives, limites, DL usuels et trigonométrie — tout au même endroit.</span></span>'
    + f'<span class="ma-banner-arrow">{_FLECHE_BANNER}</span></a>'
    + '<a class="ma-banner" href="/Entraînement" target="_top" style="animation-delay: 720ms">'
    + f'<span class="ma-banner-glyph">{_CIBLE}</span>'
    + '<span><span class="ma-banner-titre">Mode entraînement</span>'
    + '<span class="ma-banner-sous">Un exercice aléatoire, tu cherches sur papier, puis tu révèles la correction détaillée.</span></span>'
    + f'<span class="ma-banner-arrow">{_FLECHE_BANNER}</span></a>'
    + '<div class="ma-foot">MathApp v1 — moteur SymPy, rendu KaTeX</div>'
    + '</div>'
)
st.markdown(contenu, unsafe_allow_html=True)
