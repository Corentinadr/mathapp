import json
from urllib.parse import quote

import streamlit.components.v1 as components

from ui.entete import PAGES

# Mots-clés de recherche par slug (en plus du titre et du sous-titre)
_MOTS_CLES = {
    "Équation_2nd_degré": ["equation", "second degre", "discriminant", "delta", "racines", "polynome", "trinome"],
    "Dérivée": ["derivee", "deriver", "tangente", "pente", "variation", "f prime"],
    "Primitive": ["primitive", "antiderivee", "integrale indefinie"],
    "Intégrale_définie": ["integrale", "aire", "bornes", "aire sous la courbe"],
    "Limite": ["limite", "lim", "tend vers", "infini", "forme indeterminee", "hopital", "equivalents"],
    "Développement_limité": ["dl", "taylor", "young", "maclaurin", "developpement", "ordre", "approximation"],
}

_LOUPE = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'
)


def _donnees() -> str:
    items = []
    for slug, glyphe, titre, sous_titre, domaine in PAGES:
        items.append({
            "chemin": "/" + quote(slug),
            "glyphe": glyphe,
            "titre": titre,
            "sous": sous_titre,
            "termes": [titre, sous_titre, domaine] + _MOTS_CLES.get(slug, []),
        })
    items.append({
        "chemin": "/Formulaire",
        "glyphe": "§",
        "titre": "Formulaire",
        "sous": "Dérivées, primitives, limites, DL usuels, trigonométrie",
        "termes": ["formulaire", "formules usuelles", "tableau", "rappels", "cours", "trigo", "trigonometrie"],
    })
    items.append({
        "chemin": "/" + quote("Entraînement"),
        "glyphe": "?",
        "titre": "Entraînement",
        "sous": "Exercices aléatoires avec correction à révéler",
        "termes": ["entrainement", "exercice aleatoire", "quiz", "pratique", "s'entrainer", "reviser"],
    })
    return json.dumps(items, ensure_ascii=False)


def afficher_recherche(sombre: bool) -> None:
    """Barre de recherche des exercices : correspondance floue au fil de la saisie."""
    if sombre:
        c = {
            "fond": "#161619", "bord": "#26262A", "bord_focus": "#6366F1",
            "texte": "#F2F2F2", "texte2": "#9A9A9E", "hover": "#212124",
            "glyphe_bg": "rgba(99,102,241,0.16)", "glyphe_fg": "#8B8FF5",
            "ombre": "0 12px 32px rgba(0,0,0,0.5)",
        }
    else:
        c = {
            "fond": "#FFFFFF", "bord": "#EAEAEA", "bord_focus": "#4F46E5",
            "texte": "#171717", "texte2": "#737373", "hover": "#F5F5F7",
            "glyphe_bg": "#EEF0FF", "glyphe_fg": "#4F46E5",
            "ombre": "0 12px 32px rgba(0,0,0,0.08)",
        }

    html = """
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: transparent;
  font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; }
.boite { position: relative; padding: 4px; }
.champ {
  display: flex; align-items: center; gap: 10px;
  height: 46px; padding: 0 16px;
  background: __FOND__; border: 1px solid __BORD__; border-radius: 12px;
  color: __TEXTE2__; transition: all 200ms ease;
}
.champ:focus-within { border-color: __BORD_FOCUS__; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15); }
.champ input {
  flex: 1; border: none; outline: none; background: transparent;
  font-size: 14.5px; color: __TEXTE__; font-family: inherit;
}
.champ input::placeholder { color: __TEXTE2__; }
.panneau {
  position: absolute; top: 56px; left: 4px; right: 4px;
  background: __FOND__; border: 1px solid __BORD__; border-radius: 14px;
  box-shadow: __OMBRE__; padding: 6px; display: none;
}
.panneau.ouvert { display: block; }
.item {
  display: flex; align-items: center; gap: 12px;
  padding: 9px 12px; border-radius: 10px; cursor: pointer;
}
.item.actif { background: __HOVER__; }
.glyphe {
  flex: none; min-width: 40px; height: 34px; padding: 0 7px; border-radius: 10px;
  background: __GLYPHE_BG__; color: __GLYPHE_FG__;
  display: inline-flex; align-items: center; justify-content: center;
  font-family: Georgia, 'Times New Roman', serif; font-style: italic; font-size: 12.5px;
}
.titre { font-size: 14px; font-weight: 600; color: __TEXTE__; }
.sous { font-size: 12px; color: __TEXTE2__; margin-top: 1px; }
.vide { padding: 14px 12px; font-size: 13.5px; color: __TEXTE2__; text-align: center; }
</style>
<div class="boite">
  <div class="champ">__LOUPE__<input id="q" type="text"
    placeholder="Rechercher un exercice… (dérivée, DL, limite, aire…)" autocomplete="off"></div>
  <div class="panneau" id="p"></div>
</div>
<script>
var ITEMS = __DONNEES__;
var input = document.getElementById("q");
var panneau = document.getElementById("p");
var actif = 0;
var resultats = [];

function norm(s) {
  return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
}
function scoreTerme(q, t) {
  var n = norm(t);
  if (n === q) return 120;
  if (n.startsWith(q)) return 100;
  if (n.includes(" " + q)) return 85;
  var idx = n.indexOf(q);
  if (idx >= 0) return 75 - idx;
  var i = 0, trous = 0, dernier = -2;
  for (var c = 0; c < n.length && i < q.length; c++) {
    if (n[c] === q[i]) { if (dernier >= 0 && c > dernier + 1) trous++; dernier = c; i++; }
  }
  if (i === q.length) return 45 - trous * 5;
  return -1;
}
function chercher(q) {
  q = norm(q.trim());
  if (!q) return ITEMS.map(function (it) { return { it: it, s: 0 }; });
  return ITEMS.map(function (it) {
    var best = -1;
    for (var j = 0; j < it.termes.length; j++) best = Math.max(best, scoreTerme(q, it.termes[j]));
    return { it: it, s: best };
  }).filter(function (r) { return r.s >= 25; }).sort(function (a, b) { return b.s - a.s; });
}
function dessiner() {
  if (!resultats.length) {
    panneau.innerHTML = '<div class="vide">Aucun exercice trouvé</div>';
    return;
  }
  panneau.innerHTML = resultats.map(function (r, i) {
    return '<div class="item' + (i === actif ? " actif" : "") + '" data-i="' + i + '">'
      + '<span class="glyphe">' + r.it.glyphe + '</span>'
      + '<span><div class="titre">' + r.it.titre + '</div><div class="sous">' + r.it.sous + '</div></span></div>';
  }).join("");
  var items = panneau.querySelectorAll(".item");
  for (var k = 0; k < items.length; k++) {
    items[k].addEventListener("mousedown", function (e) {
      e.preventDefault();
      aller(parseInt(this.getAttribute("data-i")));
    });
    items[k].addEventListener("mousemove", function () {
      var i = parseInt(this.getAttribute("data-i"));
      if (i !== actif) { actif = i; dessiner(); }
    });
  }
}
function aller(i) {
  if (!resultats[i]) return;
  var chemin = resultats[i].it.chemin;
  /* L'iframe est sandboxée sans allow-top-navigation : on navigue via un
     lien créé dans le document parent (même origine), comme le header.
     target=_top : sur Streamlit Cloud l'app vit dans une iframe wrapper —
     naviguer la frame courante emboîterait le site dans lui-même. */
  try {
    var doc = window.parent.document;
    var a = doc.createElement("a");
    a.href = chemin;
    a.target = "_top";
    a.style.display = "none";
    doc.body.appendChild(a);
    a.click();
  } catch (e) {
    window.top.location.href = chemin;
  }
}
function ouvrir() {
  resultats = chercher(input.value);
  actif = 0;
  dessiner();
  panneau.classList.add("ouvert");
  var fr = window.frameElement;
  if (fr) {
    fr.style.height = "470px";
    fr.style.marginBottom = "-414px";
    fr.style.position = "relative";
    fr.style.zIndex = "500";
  }
}
function fermer() {
  panneau.classList.remove("ouvert");
  var fr = window.frameElement;
  if (fr) {
    fr.style.height = "56px";
    fr.style.marginBottom = "0px";
    fr.style.zIndex = "auto";
  }
}
input.addEventListener("focus", ouvrir);
input.addEventListener("input", ouvrir);
input.addEventListener("blur", function () { setTimeout(fermer, 120); });
input.addEventListener("keydown", function (e) {
  if (e.key === "ArrowDown") { e.preventDefault(); actif = Math.min(actif + 1, resultats.length - 1); dessiner(); }
  else if (e.key === "ArrowUp") { e.preventDefault(); actif = Math.max(actif - 1, 0); dessiner(); }
  else if (e.key === "Enter") { e.preventDefault(); aller(actif); }
  else if (e.key === "Escape") { input.blur(); }
});
</script>
"""
    html = (
        html.replace("__FOND__", c["fond"])
        .replace("__BORD_FOCUS__", c["bord_focus"])
        .replace("__BORD__", c["bord"])
        .replace("__TEXTE2__", c["texte2"])
        .replace("__TEXTE__", c["texte"])
        .replace("__HOVER__", c["hover"])
        .replace("__GLYPHE_BG__", c["glyphe_bg"])
        .replace("__GLYPHE_FG__", c["glyphe_fg"])
        .replace("__OMBRE__", c["ombre"])
        .replace("__LOUPE__", _LOUPE)
        .replace("__DONNEES__", _donnees())
    )
    components.html(html, height=56)
