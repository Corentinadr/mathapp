# MathApp

Application web de résolution d'exercices mathématiques de niveau supérieur (algèbre, analyse, stats) avec affichage des étapes.

## Stack
- **Python 3.11+**
- **SymPy** — moteur de calcul formel
- **Streamlit** — interface web (rendu LaTeX natif via `st.latex`)
- **pytest** — tests unitaires

## Structure

```
math-app/
├── main.py              # point d'entrée Streamlit (streamlit run main.py)
├── core/                # types partagés + parsing d'expressions
├── solvers/             # un sous-package par domaine
│   ├── algebre/
│   ├── analyse/
│   └── stats/
├── ui/                  # composants Streamlit réutilisables
└── tests/               # pytest
```

## Conventions

### Solveurs
- Chaque solveur expose une fonction publique qui prend une **expression SymPy** (ou string parsable) et des **paramètres nommés**, retourne un objet `Solution`.
- Ne jamais imprimer / afficher depuis un solveur — retourner de la donnée structurée.
- Les étapes intermédiaires sont des `Step` avec un `title` (str) et une `expression` (SymPy) pour rendu LaTeX.

### Types (`core/types.py`)
- `Exercise` : énoncé + paramètres d'entrée
- `Step` : une étape de résolution (titre + expression SymPy)
- `Solution` : résultat final + liste de `Step`

### Style
- Type hints partout
- Noms français pour les concepts métier (`derivee`, `integrale`), anglais pour l'infra (`parser`, `solver`)

### UI (`ui/`)
- Chaque page commence par `configurer_page("Titre")` (`ui/config.py`) : favicon, thème, header fixe custom. L'accueil appelle `configurer_page()` sans argument (layout large).
- Navigation via le header custom (`ui/entete.py`, source de vérité `PAGES`) — la sidebar Streamlit est masquée. Nouvelle page = ajouter une entrée dans `PAGES` + un fichier `pages/N_Titre.py`.
- Thèmes clair + sombre : palettes widgets dans `.streamlit/config.toml` (`[theme.light]` / `[theme.dark]`). Le CSS custom n'utilise **jamais** de couleur en dur : uniquement des variables `var(--ma-*)`, définies selon le thème résolu (`st.context.theme.type`) dans `ui/style.py`. Nouvelle couleur = l'ajouter aux deux palettes (`_VARS_CLAIR` / `_VARS_SOMBRE`).
- Bascule clair/sombre : bouton dans le header (`ui/bascule.py`, iframe `components.html`) qui écrit `stActiveTheme-<chemin>-v2` dans le localStorage **pour tous les chemins** puis recharge. Nouvelle page = son chemin est couvert automatiquement via `PAGES` (sauf pages hors `PAGES`, à ajouter à la main dans `bascule.py` comme `/Formulaire`).
- Champs de saisie de fonctions : `st.selectbox(..., accept_new_options=True)` avec des exemples adaptés à l'exercice, jamais un `text_input` nu.

## Commandes

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
streamlit run main.py

# Tests
pytest tests/
```

## Développement
- **Tranches verticales** : un type d'exercice doit marcher de bout en bout (solveur → UI → test) avant d'en ajouter un autre.
- Toujours écrire un test pour un nouveau solveur, même minimal.
