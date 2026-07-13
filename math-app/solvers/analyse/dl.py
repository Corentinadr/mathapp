import sympy as sp

from core.parser import parse
from core.types import Solution, Step


def developpement_limite(
    expression: str,
    point: str = "0",
    ordre: int = 5,
    variable: str = "x",
) -> Solution:
    """Développement limité de `expression` autour de `point` à l'ordre `ordre`."""
    if ordre < 1:
        raise ValueError("L'ordre doit être ≥ 1.")

    var = sp.Symbol(variable)
    f = parse(expression)
    a = parse(str(point))

    etapes: list[Step] = [
        Step(
            f"Fonction f({variable})",
            sp.Eq(sp.Function("f")(var), f),
            explication=(
                r"L'idée du **développement limité** : approcher $f$ au voisinage de $a$ par un "
                r"polynôme, plus un **reste** négligeable devant $(x-a)^n$."
            ),
        ),
        Step(
            f"Formule de Taylor-Young à l'ordre {ordre} autour de {variable} = {a}",
            sp.Function("f")(var),
            explication=(
                r"On applique la **formule de Taylor-Young** : "
                rf"$\displaystyle f({variable}) = \sum_{{k=0}}^{{{ordre}}} "
                rf"\dfrac{{f^{{(k)}}({sp.latex(a)})}}{{k!}} \bigl({variable} - {sp.latex(a)}\bigr)^k "
                rf"+ o\bigl(({variable}-{sp.latex(a)})^{{{ordre}}}\bigr)$. "
                "SymPy calcule les dérivées successives de $f$ en $a$, puis assemble le polynôme."
            ),
        ),
    ]

    serie = sp.series(f, var, a, ordre + 1)
    etapes.append(
        Step(
            "Série avec reste",
            sp.Eq(sp.Function("f")(var), serie),
            explication=(
                rf"La notation $O\bigl(({variable}-{sp.latex(a)})^{{{ordre + 1}}}\bigr)$ désigne le **reste** : "
                r"une fonction dont on sait juste qu'elle est négligeable devant le dernier terme conservé."
            ),
        )
    )

    polynome = serie.removeO()
    etapes.append(
        Step(
            "Polynôme du développement (sans reste)",
            sp.Eq(sp.Function("f")(var), polynome),
            explication=(
                "En pratique on ne garde que la partie polynomiale : c'est **elle** qui sert pour "
                "calculer des limites, étudier une position par rapport à la tangente, prouver des "
                "équivalents, etc."
            ),
        )
    )

    return Solution(resultat=serie, etapes=etapes)
