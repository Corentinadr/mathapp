import sympy as sp

from core.types import Solution, Step

x = sp.Symbol("x")


def resoudre_second_degre(a: float, b: float, c: float) -> Solution:
    """Résout ax² + bx + c = 0 et détaille les étapes (discriminant + racines)."""
    if a == 0:
        raise ValueError("a doit être non nul (sinon ce n'est pas une équation du 2nd degré).")

    A, B, C = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
    equation = sp.Eq(A * x**2 + B * x + C, 0)
    delta = B**2 - 4 * A * C

    etapes: list[Step] = [
        Step(
            "Équation de départ",
            equation,
            explication=(
                "On reconnaît une équation polynomiale de degré 2 de la forme "
                r"$ax^2 + bx + c = 0$ avec $a \neq 0$. On applique la **méthode du discriminant**."
            ),
        ),
        Step(
            "Calcul du discriminant Δ = b² - 4ac",
            sp.Eq(sp.Symbol("Delta"), delta),
            explication=(
                r"Le discriminant $\Delta$ indique le nombre et la nature des solutions **sans avoir "
                r"à les calculer**. C'est son signe qui décide."
            ),
        ),
    ]

    if delta > 0:
        r1 = sp.simplify((-B - sp.sqrt(delta)) / (2 * A))
        r2 = sp.simplify((-B + sp.sqrt(delta)) / (2 * A))
        etapes.append(
            Step(
                "Δ > 0 : deux racines réelles distinctes",
                sp.Symbol("Delta") > 0,
                explication=(
                    r"Quand $\Delta > 0$, l'équation admet **deux solutions réelles** distinctes, "
                    r"données par $x = \dfrac{-b \pm \sqrt{\Delta}}{2a}$."
                ),
            )
        )
        etapes.append(
            Step(
                "x₁ = (-b - √Δ) / 2a",
                sp.Eq(sp.Symbol("x_1"), r1),
                explication=(
                    rf"On applique la formule avec $a={sp.latex(A)}$, $b={sp.latex(B)}$, "
                    rf"$\Delta={sp.latex(delta)}$."
                ),
            )
        )
        etapes.append(
            Step(
                "x₂ = (-b + √Δ) / 2a",
                sp.Eq(sp.Symbol("x_2"), r2),
                explication="Deuxième racine avec le signe $+$ devant la racine carrée.",
            )
        )
        return Solution(resultat=[r1, r2], etapes=etapes)

    if delta == 0:
        r = sp.simplify(-B / (2 * A))
        etapes.append(
            Step(
                "Δ = 0 : une racine double",
                sp.Eq(sp.Symbol("Delta"), 0),
                explication=(
                    r"Quand $\Delta = 0$, l'équation admet **une seule solution réelle**, "
                    r"dite « racine double » : $x = -\dfrac{b}{2a}$."
                ),
            )
        )
        etapes.append(
            Step(
                "x = -b / 2a",
                sp.Eq(sp.Symbol("x_0"), r),
                explication="La formule générale se simplifie car $\\sqrt{\\Delta} = 0$.",
            )
        )
        return Solution(resultat=[r], etapes=etapes)

    r1 = sp.simplify((-B - sp.sqrt(delta)) / (2 * A))
    r2 = sp.simplify((-B + sp.sqrt(delta)) / (2 * A))
    etapes.append(
        Step(
            "Δ < 0 : deux racines complexes conjuguées",
            sp.Symbol("Delta") < 0,
            explication=(
                r"Quand $\Delta < 0$, **aucune solution réelle**. En passant dans $\mathbb{C}$ "
                r"avec $i^2 = -1$, on trouve deux racines conjuguées "
                r"$x = \dfrac{-b \pm i\sqrt{|\Delta|}}{2a}$."
            ),
        )
    )
    etapes.append(
        Step(
            "x₁ = (-b - i√|Δ|) / 2a",
            sp.Eq(sp.Symbol("x_1"), r1),
            explication="Racine complexe avec le signe $-$.",
        )
    )
    etapes.append(
        Step(
            "x₂ = (-b + i√|Δ|) / 2a",
            sp.Eq(sp.Symbol("x_2"), r2),
            explication="Racine conjuguée de $x_1$.",
        )
    )
    return Solution(resultat=[r1, r2], etapes=etapes)
