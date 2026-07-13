"""Tracé des fonctions avec matplotlib, stylé selon le thème de l'app."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import sympy as sp

_SEUIL_SINGULARITE = 1e6


def _palette(sombre: bool) -> dict[str, str]:
    if sombre:
        return {"texte": "#9A9A9E", "grille": "#26262A", "accent": "#8B8FF5", "second": "#9A9A9E"}
    return {"texte": "#737373", "grille": "#EAEAEA", "accent": "#4F46E5", "second": "#A3A3A3"}


def _evaluer(expr: sp.Expr, variable: sp.Symbol, x: np.ndarray) -> np.ndarray | None:
    """Évalue expr sur x en masquant valeurs complexes et singularités (NaN)."""
    try:
        f = sp.lambdify(variable, expr, modules=["numpy"])
        with np.errstate(all="ignore"):
            y = np.asarray(f(x), dtype=complex)
    except Exception:
        return None
    if y.shape != x.shape:  # expression constante
        y = np.full_like(x, complex(y))
    reel = np.where(np.abs(y.imag) < 1e-9, y.real, np.nan)
    reel = np.where(np.abs(reel) > _SEUIL_SINGULARITE, np.nan, reel)
    return reel


def tracer(
    courbes: list[tuple[sp.Expr, str]],
    variable: sp.Symbol,
    x_min: float,
    x_max: float,
    sombre: bool,
    remplissage: tuple[float, float] | None = None,
    points: list[tuple[float, float]] | None = None,
    titre: str = "Visualisation",
) -> None:
    """Trace une ou plusieurs courbes ; ne rien afficher si aucune n'est évaluable.

    `courbes` : [(expression, légende)] — la première en accent plein, les suivantes en tirets.
    `remplissage` : (a, b) → aire sous la première courbe coloriée entre a et b.
    `points` : [(x, y)] marqués sur le graphe.
    """
    pal = _palette(sombre)
    x = np.linspace(float(x_min), float(x_max), 800)

    traces = []
    for expr, legende in courbes:
        y = _evaluer(expr, variable, x)
        if y is not None and np.isfinite(y).any():
            traces.append((y, legende))
    if not traces:
        return

    fig, ax = plt.subplots(figsize=(7, 3.4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    styles = [
        {"color": pal["accent"], "linewidth": 2.2},
        {"color": pal["second"], "linewidth": 1.8, "linestyle": "--"},
        {"color": pal["second"], "linewidth": 1.5, "linestyle": ":"},
    ]
    for (y, legende), style in zip(traces, styles):
        ax.plot(x, y, label=legende, **style)

    if remplissage is not None:
        a, b = remplissage
        masque = (x >= float(a)) & (x <= float(b))
        ax.fill_between(x[masque], traces[0][0][masque], color=pal["accent"], alpha=0.22, linewidth=0)

    if points:
        for px, py in points:
            ax.plot([px], [py], "o", color=pal["accent"], markersize=6, zorder=5)

    ax.axhline(0, color=pal["grille"], linewidth=1)
    ax.axvline(0, color=pal["grille"], linewidth=1)
    ax.grid(color=pal["grille"], linewidth=0.5, alpha=0.6)
    for cote in ("top", "right", "bottom", "left"):
        ax.spines[cote].set_visible(False)
    ax.tick_params(colors=pal["texte"], labelsize=9)
    legende = ax.legend(frameon=False, fontsize=9, labelcolor=pal["texte"])

    # Limiter l'axe y aux valeurs "raisonnables" pour rester lisible malgré les asymptotes
    valeurs = np.concatenate([y[np.isfinite(y)] for y, _ in traces])
    if valeurs.size:
        bas, haut = np.percentile(valeurs, [2, 98])
        marge = max((haut - bas) * 0.15, 0.5)
        ax.set_ylim(bas - marge, haut + marge)

    st.subheader(titre)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
