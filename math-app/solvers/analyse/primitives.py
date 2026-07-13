import sympy as sp

from core.parser import parse
from core.types import Solution, Step


def primitiver(expression: str, variable: str = "x") -> Solution:
    """Calcule une primitive de l'expression par rapport à `variable`."""
    var = sp.Symbol(variable)
    f = parse(expression)

    etapes: list[Step] = [
        Step(
            f"Fonction f({variable})",
            sp.Eq(sp.Function("f")(var), f),
            explication=(
                r"On cherche une fonction $F$ telle que $F'(x) = f(x)$. "
                "Techniques appliquées dans l'ordre : **primitives usuelles** (voir formulaire), "
                "**linéarité** ($\\int (u + v) = \\int u + \\int v$), **changement de variable**, "
                "**intégration par parties** ($\\int u'v = uv - \\int uv'$), "
                "et **décomposition en éléments simples** pour les fractions rationnelles."
            ),
        ),
        Step(
            f"Recherche de F telle que F'({variable}) = f({variable})",
            sp.Eq(sp.Function("F")(var), sp.Integral(f, var)),
            explication=(
                r"On note l'intégrale sans bornes. Le résultat est défini **à une constante $C$ près** "
                r"(car deux primitives d'une même fonction diffèrent d'une constante)."
            ),
        ),
    ]

    F = sp.integrate(f, var)

    if F.has(sp.Integral):
        etapes.append(
            Step(
                "SymPy ne trouve pas de forme close pour cette primitive.",
                F,
                explication=(
                    "Certaines fonctions n'admettent pas de primitive exprimable avec les fonctions "
                    "usuelles (ex : $e^{-x^2}$). SymPy retourne alors l'intégrale telle quelle."
                ),
            )
        )
        return Solution(resultat=F, etapes=etapes)

    simplifiee = sp.simplify(F)
    if simplifiee != F:
        etapes.append(
            Step(
                "Primitive calculée",
                sp.Eq(sp.Function("F")(var), F),
                explication="Résultat brut avant simplification.",
            )
        )
        etapes.append(
            Step(
                "Forme simplifiée (+ constante d'intégration)",
                sp.Eq(sp.Function("F")(var), simplifiee + sp.Symbol("C")),
                explication=r"On ajoute $+ C$ pour représenter **toutes** les primitives possibles.",
            )
        )
        resultat = simplifiee + sp.Symbol("C")
    else:
        etapes.append(
            Step(
                "Primitive (+ constante d'intégration)",
                sp.Eq(sp.Function("F")(var), F + sp.Symbol("C")),
                explication=r"On ajoute $+ C$ pour représenter **toutes** les primitives possibles.",
            )
        )
        resultat = F + sp.Symbol("C")

    return Solution(resultat=resultat, etapes=etapes)
