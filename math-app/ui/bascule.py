from urllib.parse import quote

import streamlit.components.v1 as components

from ui.entete import PAGES

_SOLEIL = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/>'
    '<path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/>'
    '<path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/>'
    '<path d="m19.07 4.93-1.41 1.41"/></svg>'
)

_LUNE = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>'
)


def afficher_bascule(sombre: bool) -> None:
    """Bouton clair/sombre fixé dans le header (iframe positionnée par le CSS global).

    Écrit le thème choisi dans le localStorage de Streamlit (clé par chemin de page,
    pour que le choix tienne en naviguant), puis recharge la page.

    Les clés sont dérivées du chemin réel de la frame Streamlit : en local les pages
    vivent sur « /Dérivée », mais sur Streamlit Cloud l'app est embarquée dans une
    iframe sur « /~/+/Dérivée » — des chemins codés en dur n'y correspondraient jamais.
    """
    cible = "Light" if sombre else "Dark"
    icone = _SOLEIL if sombre else _LUNE
    titre = "Passer en mode clair" if sombre else "Passer en mode sombre"

    slugs = ['"Formulaire"', f'"{quote("Entraînement")}"'] + [
        f'"{quote(slug)}"' for slug, *_ in PAGES
    ]

    if sombre:
        fg, border, bg, hover_fg = "#A3A3A8", "#333338", "rgba(23, 23, 26, 0.6)", "#ECECEC"
    else:
        fg, border, bg, hover_fg = "#525252", "#E0E0E0", "rgba(255, 255, 255, 0.6)", "#171717"

    html = (
        "<style>"
        "html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; }"
        "button {"
        f"  width: 36px; height: 36px; border-radius: 10px;"
        f"  border: 1px solid {border}; background: {bg}; color: {fg};"
        "  display: flex; align-items: center; justify-content: center;"
        "  cursor: pointer; transition: all 200ms ease; padding: 0;"
        "}"
        f"button:hover {{ color: {hover_fg}; transform: scale(1.08) rotate(12deg); }}"
        "</style>"
        f'<button id="bascule" title="{titre}" aria-label="{titre}">{icone}</button>'
        "<script>"
        'document.getElementById("bascule").addEventListener("click", function () {'
        f"  var valeur = JSON.stringify('{cible}');"
        f"  var slugs = [{', '.join(slugs)}];"
        "  try {"
        "    var stockage = window.parent.localStorage;"
        "    var chemin = window.parent.location.pathname;"
        "    var base = chemin;"
        "    for (var i = 0; i < slugs.length; i++) {"
        '      if (base.slice(-slugs[i].length - 1) === "/" + slugs[i]) {'
        "        base = base.slice(0, base.length - slugs[i].length);"
        "        break;"
        "      }"
        "    }"
        '    if (base.slice(-1) !== "/") base += "/";'
        "    var cles = [base];"
        "    for (var i = 0; i < slugs.length; i++) cles.push(base + slugs[i]);"
        "    for (var i = 0; i < cles.length; i++) {"
        '      stockage.setItem("stActiveTheme-" + cles[i] + "-v2", valeur);'
        "    }"
        "    for (var i = stockage.length - 1; i >= 0; i--) {"
        "      var k = stockage.key(i);"
        '      if (k && k.indexOf("stActiveTheme-") === 0) stockage.setItem(k, valeur);'
        "    }"
        "    window.parent.location.reload();"
        "  } catch (e) { console.error(e); }"
        "});"
        "</script>"
    )
    components.html(html, height=38)
