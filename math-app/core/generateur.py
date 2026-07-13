"""Génération d'exercices aléatoires pour le mode entraînement."""

import random

import sympy as sp

from core.parser import parse
from core.types import Solution
from solvers.algebre.equations import resoudre_second_degre
from solvers.analyse.derivees import deriver
from solvers.analyse.dl import developpement_limite
from solvers.analyse.limites import calculer_limite
from solvers.analyse.primitives import primitiver

TYPES = ["equation", "derivee", "primitive", "limite", "dl"]

x = sp.Symbol("x")


def _generer_equation() -> dict:
    a = random.choice([1, 1, 2, -1])
    if random.random() < 0.7:  # racines réelles entières
        r1, r2 = random.randint(-5, 5), random.randint(-5, 5)
        b, c = -a * (r1 + r2), a * r1 * r2
    else:  # discriminant négatif
        k, m = random.randint(-3, 3), random.randint(1, 5)
        b, c = 2 * a * k, a * (k * k) + m
    trinome = a * x**2 + b * x + c
    return {
        "type": "equation",
        "consigne": "Résous dans ℂ :",
        "latex": sp.latex(sp.Eq(trinome, 0)),
        "params": {"a": float(a), "b": float(b), "c": float(c)},
    }


def _generer_derivee() -> dict:
    k, n = random.randint(2, 4), random.randint(2, 3)
    modeles = [
        f"{k}x^3 - {n}x^2 + {random.randint(1, 6)}x - {random.randint(1, 9)}",
        f"sin({k}x)",
        f"x^{n} * exp(x)",
        "log(x) / x",
        f"sqrt(1 + {k}x^2)",
        f"x^2 * cos({k}x)",
        f"exp({k}x) / x",
    ]
    expression = random.choice(modeles)
    ordre = random.choice([1, 1, 1, 2])
    consigne = "Calcule $f'(x)$ pour :" if ordre == 1 else "Calcule $f''(x)$ pour :"
    return {
        "type": "derivee",
        "consigne": consigne,
        "latex": "f(x) = " + sp.latex(parse(expression)),
        "params": {"expression": expression, "variable": "x", "ordre": ordre},
    }


def _generer_primitive() -> dict:
    k = random.randint(2, 5)
    modeles = [
        f"{k}x^2 + {random.randint(1, 6)}x + {random.randint(1, 9)}",
        f"cos({k}x)",
        "x * exp(x)",
        "1 / (1 + x^2)",
        "sin(x)^2",
        f"{k} / x",
        f"x * sin({k}x)",
    ]
    expression = random.choice(modeles)
    return {
        "type": "primitive",
        "consigne": "Détermine une primitive de :",
        "latex": "f(x) = " + sp.latex(parse(expression)),
        "params": {"expression": expression, "variable": "x"},
    }


def _generer_limite() -> dict:
    k = random.randint(2, 5)
    modeles = [
        (f"sin({k}x) / x", "0"),
        ("(1 - cos(x)) / x^2", "0"),
        (f"(exp({k}x) - 1) / x", "0"),
        (f"(1 + {k}/x)^x", "oo"),
        (f"log(1 + {k}x) / x", "0"),
        (f"x^{random.randint(1, 3)} * exp(-x)", "oo"),
        (f"(x^2 - {k * k}) / (x - {k})", str(k)),
    ]
    expression, point = random.choice(modeles)
    f = parse(expression)
    a = parse(point)
    return {
        "type": "limite",
        "consigne": "Calcule la limite :",
        "latex": sp.latex(sp.Limit(f, x, a)),
        "params": {"expression": expression, "point": point, "variable": "x", "direction": "deux côtés"},
    }


def _generer_dl() -> dict:
    fonctions = ["exp(x)", "sin(x)", "cos(x)", "log(1 + x)", "1 / (1 - x)", "sqrt(1 + x)", "tan(x)"]
    expression = random.choice(fonctions)
    ordre = random.randint(2, 4)
    return {
        "type": "dl",
        "consigne": f"Donne le développement limité **à l'ordre {ordre} en 0** de :",
        "latex": "f(x) = " + sp.latex(parse(expression)),
        "params": {"expression": expression, "point": "0", "ordre": ordre, "variable": "x"},
    }


_GENERATEURS = {
    "equation": _generer_equation,
    "derivee": _generer_derivee,
    "primitive": _generer_primitive,
    "limite": _generer_limite,
    "dl": _generer_dl,
}


def generer(type_exercice: str | None = None) -> dict:
    """Génère un exercice aléatoire ; type au hasard si None."""
    if type_exercice is None:
        type_exercice = random.choice(TYPES)
    if type_exercice not in _GENERATEURS:
        raise ValueError(f"Type inconnu : {type_exercice}. Attendu : {TYPES}.")
    return _GENERATEURS[type_exercice]()


def resoudre(exo: dict) -> Solution:
    """Résout un exercice généré avec le solveur correspondant."""
    p = exo["params"]
    match exo["type"]:
        case "equation":
            return resoudre_second_degre(p["a"], p["b"], p["c"])
        case "derivee":
            return deriver(p["expression"], variable=p["variable"], ordre=p["ordre"])
        case "primitive":
            return primitiver(p["expression"], variable=p["variable"])
        case "limite":
            return calculer_limite(p["expression"], p["point"], variable=p["variable"], direction=p["direction"])
        case "dl":
            return developpement_limite(p["expression"], point=p["point"], ordre=p["ordre"], variable=p["variable"])
    raise ValueError(f"Type inconnu : {exo['type']}.")
