import sympy as sp

from core.parser import parse
from core.types import Solution, Step

_DIRECTIONS = {"deux côtés": "+-", "à gauche": "-", "à droite": "+"}


def calculer_limite(
    expression: str,
    point: str,
    variable: str = "x",
    direction: str = "deux côtés",
) -> Solution:
    """Calcule la limite de `expression` quand `variable` tend vers `point`.

    `direction` : "deux côtés", "à gauche", "à droite".
    `point` : nombre, "oo", "-oo", "pi", etc.
    """
    if direction not in _DIRECTIONS:
        raise ValueError(f"Direction inconnue : {direction}. Attendu : {list(_DIRECTIONS)}.")

    var = sp.Symbol(variable)
    f = parse(expression)
    a = parse(str(point))
    dir_sym = _DIRECTIONS[direction]

    etapes: list[Step] = [
        Step(
            f"Fonction f({variable})",
            sp.Eq(sp.Function("f")(var), f),
            explication=(
                r"Pour $\lim_{x \to a} f(x)$, on tente d'abord la **substitution directe** "
                r"(remplacer $x$ par $a$). Si on obtient un nombre fini, c'est la limite. "
                r"Sinon on est face à une **forme indéterminée** qu'il faut lever."
            ),
        ),
        Step(
            f"Limite recherchée ({direction}, {variable} → {a})",
            sp.Limit(f, var, a, dir=dir_sym),
            explication=(
                r"La limite **bilatérale** existe si et seulement si les limites à gauche "
                r"et à droite coïncident. Pour des points de discontinuité comme $\dfrac{1}{x}$ en 0, "
                r"il faut préciser la direction."
            ),
        ),
    ]

    substitution_directe = f.subs(var, a)
    if substitution_directe.is_finite and not substitution_directe.has(sp.nan, sp.zoo):
        etapes.append(
            Step(
                "Substitution directe",
                sp.Eq(sp.Function("f")(a), substitution_directe, evaluate=False),
                explication="La substitution donne un résultat fini : c'est **directement** la limite.",
            )
        )
    else:
        # evaluate=False : sinon Eq(f(a), nan) s'auto-évalue en False
        etapes.append(
            Step(
                "Substitution directe : forme indéterminée",
                sp.Eq(sp.Function("f")(a), substitution_directe, evaluate=False),
                explication=(
                    r"On obtient une **forme indéterminée** : $\tfrac{0}{0}$, $\tfrac{\infty}{\infty}$, "
                    r"$0 \times \infty$, $\infty - \infty$, $0^0$, $\infty^0$ ou $1^\infty$. "
                    r"Il faut alors lever l'indétermination : équivalents, développements limités, "
                    r"règle de L'Hôpital, factorisation, croissances comparées…"
                ),
            )
        )

    if dir_sym == "+-":
        resultat = sp.limit(f, var, a)
    else:
        resultat = sp.limit(f, var, a, dir=dir_sym)

    etapes.append(
        Step(
            "Limite calculée",
            sp.Eq(sp.Symbol("L"), resultat),
            explication=(
                "Résultat obtenu par SymPy (typiquement via équivalents, développements limités "
                "ou croissances comparées — voir le formulaire pour les limites usuelles)."
            ),
        )
    )

    return Solution(resultat=resultat, etapes=etapes)
