import sympy as sp

from core.parser import parse
from core.types import Solution, Step


def integrer(expression: str, borne_inf: str, borne_sup: str, variable: str = "x") -> Solution:
    """Calcule l'intégrale définie de `expression` entre borne_inf et borne_sup."""
    var = sp.Symbol(variable)
    f = parse(expression)
    a = parse(str(borne_inf))
    b = parse(str(borne_sup))

    etapes: list[Step] = [
        Step(
            "Intégrale à calculer",
            sp.Eq(sp.Symbol("I"), sp.Integral(f, (var, a, b))),
            explication=(
                r"On applique le **théorème fondamental de l'analyse** : "
                r"$\displaystyle \int_a^b f(x)\, dx = F(b) - F(a)$, où $F$ est **une** primitive quelconque de $f$. "
                r"La constante $+C$ n'a pas d'importance ici car elle disparaît dans la différence."
            ),
        ),
    ]

    F = sp.integrate(f, var)

    if F.has(sp.Integral):
        valeur = sp.integrate(f, (var, a, b))
        etapes.append(
            Step(
                "Pas de primitive en forme close, calcul direct",
                valeur,
                explication=(
                    "Certaines intégrales définies se calculent sans passer par une primitive "
                    "explicite (par symétrie, contour complexe, séries…). SymPy s'en charge."
                ),
            )
        )
        return Solution(resultat=valeur, etapes=etapes)

    etapes.append(
        Step(
            f"Primitive F({variable})",
            sp.Eq(sp.Function("F")(var), sp.simplify(F)),
            explication="On calcule d'abord une primitive quelconque de $f$.",
        )
    )

    F_b = F.subs(var, b)
    F_a = F.subs(var, a)
    etapes.append(
        Step(
            f"Évaluation : F({b}) - F({a})",
            sp.Eq(sp.Symbol("I"), F_b - F_a),
            explication="On évalue $F$ aux deux bornes puis on effectue la différence.",
        )
    )

    valeur = sp.simplify(F_b - F_a)
    etapes.append(
        Step(
            "Résultat simplifié",
            sp.Eq(sp.Symbol("I"), valeur),
            explication="Simplification finale.",
        )
    )

    return Solution(resultat=valeur, etapes=etapes)
