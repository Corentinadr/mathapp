from functools import reduce

import sympy as sp

from core.parser import parse
from core.types import Solution, Step

# Au-delà de cette profondeur, on dérive sans détailler (lisibilité des étapes)
_PROFONDEUR_MAX = 4


def _forme_reduite(expr: sp.Expr) -> sp.Expr:
    """Forme la plus réduite/factorisée : simplify, puis factor si ça n'alourdit pas l'écriture."""
    simplifiee = sp.simplify(expr)
    try:
        factorisee = sp.factor(simplifiee)
    except Exception:
        return simplifiee
    return factorisee if sp.count_ops(factorisee) <= sp.count_ops(simplifiee) else simplifiee


def _facteur_commun(expr: sp.Expr) -> sp.Expr:
    """PGCD des termes d'une somme (1 si pas de somme ou pas de facteur commun)."""
    termes = sp.Add.make_args(expr)
    if len(termes) < 2:
        return sp.S.One
    try:
        return reduce(sp.gcd, termes)
    except Exception:
        return sp.S.One


def _D(expr: sp.Expr, var: sp.Symbol) -> sp.Derivative:
    return sp.Derivative(expr, var, evaluate=False)


def _eq(gauche: sp.Expr, droite: sp.Expr) -> sp.Equality:
    return sp.Eq(gauche, droite, evaluate=False)


def _deriver_detaille(expr: sp.Expr, var: sp.Symbol, etapes: list[Step], profondeur: int = 1) -> sp.Expr:
    """Dérive `expr` en expliquant la règle appliquée à chaque nœud de l'arbre."""
    if not expr.has(var):
        if profondeur <= 2:
            etapes.append(
                Step(
                    "Dérivée d'une constante",
                    _eq(_D(expr, var), sp.S.Zero),
                    explication=rf"${sp.latex(expr)}$ ne dépend pas de ${sp.latex(var)}$ : sa dérivée est nulle.",
                )
            )
        return sp.S.Zero

    if expr == var:
        return sp.S.One

    if profondeur > _PROFONDEUR_MAX:
        return sp.diff(expr, var)

    if expr.is_Add:
        etapes.append(
            Step(
                "Linéarité de la dérivation",
                _eq(_D(expr, var), sp.Add(*[_D(t, var) for t in expr.args], evaluate=False)),
                explication=r"La dérivée d'une somme est la somme des dérivées : $(u + v)' = u' + v'$. "
                "On dérive chaque terme séparément.",
            )
        )
        return sp.Add(*[_deriver_detaille(t, var, etapes, profondeur + 1) for t in expr.args])

    if expr.is_Mul:
        constante, reste = expr.as_independent(var)
        if constante != 1 and reste != 1:
            etapes.append(
                Step(
                    "Facteur constant",
                    _eq(_D(expr, var), sp.Mul(constante, _D(reste, var), evaluate=False)),
                    explication=rf"$(c \cdot u)' = c \cdot u'$ : le facteur ${sp.latex(constante)}$ "
                    "sort de la dérivation.",
                )
            )
            return constante * _deriver_detaille(reste, var, etapes, profondeur + 1)

        num, den = expr.as_numer_denom()
        if den.has(var) and den != 1:
            etapes.append(
                Step(
                    "Règle du quotient",
                    _eq(
                        _D(expr, var),
                        (_D(num, var) * den - num * _D(den, var)) / den**2,
                    ),
                    explication=rf"$\left(\dfrac{{u}}{{v}}\right)' = \dfrac{{u'v - uv'}}{{v^2}}$ "
                    rf"avec $u = {sp.latex(num)}$ et $v = {sp.latex(den)}$.",
                )
            )
            d_num = _deriver_detaille(num, var, etapes, profondeur + 1)
            d_den = _deriver_detaille(den, var, etapes, profondeur + 1)
            return (d_num * den - num * d_den) / den**2

        u, v = expr.args[0], sp.Mul(*expr.args[1:])
        etapes.append(
            Step(
                "Règle du produit",
                _eq(_D(expr, var), _D(u, var) * v + u * _D(v, var)),
                explication=rf"$(u \cdot v)' = u'v + uv'$ avec $u = {sp.latex(u)}$ et $v = {sp.latex(v)}$.",
            )
        )
        d_u = _deriver_detaille(u, var, etapes, profondeur + 1)
        d_v = _deriver_detaille(v, var, etapes, profondeur + 1)
        return d_u * v + u * d_v

    if expr.is_Pow:
        base, expo = expr.args
        if not expo.has(var):
            if base == var:
                resultat = expo * base ** (expo - 1)
                etapes.append(
                    Step(
                        "Règle de la puissance",
                        _eq(_D(expr, var), resultat),
                        explication=rf"$(x^n)' = n\,x^{{n-1}}$ avec $n = {sp.latex(expo)}$.",
                    )
                )
                return resultat
            etapes.append(
                Step(
                    "Puissance composée (règle de la chaîne)",
                    _eq(_D(expr, var), expo * base ** (expo - 1) * _D(base, var)),
                    explication=rf"$(u^n)' = n\,u^{{n-1}} \cdot u'$ avec $u = {sp.latex(base)}$ "
                    rf"et $n = {sp.latex(expo)}$.",
                )
            )
            return expo * base ** (expo - 1) * _deriver_detaille(base, var, etapes, profondeur + 1)

        if not base.has(var):
            etapes.append(
                Step(
                    "Exponentielle de base constante",
                    _eq(_D(expr, var), expr * sp.log(base) * _D(expo, var)),
                    explication=rf"$(a^u)' = a^u \ln a \cdot u'$ avec $a = {sp.latex(base)}$ "
                    rf"et $u = {sp.latex(expo)}$.",
                )
            )
            return expr * sp.log(base) * _deriver_detaille(expo, var, etapes, profondeur + 1)

        etapes.append(
            Step(
                "Puissance de la forme f(x)^g(x)",
                _eq(expr, sp.exp(expo * sp.log(base))),
                explication=r"On réécrit $f^g = e^{g \ln f}$ puis on dérive cette exponentielle composée.",
            )
        )
        return sp.diff(expr, var)

    if isinstance(expr, sp.Function) and len(expr.args) == 1:
        interne = expr.args[0]
        u = sp.Symbol("u")
        try:
            derivee_exterieure = expr.func(u).diff(u)
        except Exception:
            return sp.diff(expr, var)

        if interne == var:
            resultat = derivee_exterieure.subs(u, var)
            etapes.append(
                Step(
                    "Dérivée usuelle",
                    _eq(_D(expr, var), resultat),
                    explication="Dérivée directe du tableau des dérivées usuelles (voir le formulaire).",
                )
            )
            return resultat

        exterieure_en_interne = derivee_exterieure.subs(u, interne)
        etapes.append(
            Step(
                "Règle de la chaîne",
                _eq(_D(expr, var), _D(interne, var) * exterieure_en_interne),
                explication=rf"$(f \circ u)'(x) = u'(x) \cdot f'(u)$ avec $u = {sp.latex(interne)}$ "
                rf"et $f'(u) = {sp.latex(derivee_exterieure)}$.",
            )
        )
        return _deriver_detaille(interne, var, etapes, profondeur + 1) * exterieure_en_interne

    etapes.append(
        Step(
            "Dérivation directe",
            _eq(_D(expr, var), sp.diff(expr, var)),
            explication="Cas non détaillé : SymPy applique directement ses règles internes.",
        )
    )
    return sp.diff(expr, var)


def deriver(expression: str, variable: str = "x", ordre: int = 1) -> Solution:
    """Dérive une expression en détaillant chaque règle appliquée (ordre 1),
    puis dérive successivement pour les ordres supérieurs."""
    if ordre < 1:
        raise ValueError("L'ordre doit être ≥ 1.")

    var = sp.Symbol(variable)
    f = parse(expression)

    etapes: list[Step] = [
        Step(
            f"Fonction f({variable})",
            sp.Eq(sp.Function("f")(var), f),
            explication=(
                "On identifie la **structure** de l'expression (somme, produit, quotient, "
                "composition…) pour choisir la règle de dérivation à appliquer à chaque niveau."
            ),
        ),
    ]

    brute = _deriver_detaille(f, var, etapes)
    etapes.append(
        Step(
            "Assemblage",
            _eq(_D(f, var), brute),
            explication="On remonte les morceaux dérivés dans la formule de départ.",
        )
    )

    resultat = _forme_reduite(brute)
    if resultat != brute:
        facteur = _facteur_commun(brute)
        if facteur not in (sp.S.One, sp.S.NegativeOne):
            etapes.append(
                Step(
                    "Factorisation",
                    sp.Eq(sp.Symbol(f"f'({variable})"), resultat),
                    explication=(
                        rf"Chaque terme contient le facteur commun ${sp.latex(facteur)}$ : "
                        "on le met en évidence, puis on réduit ce qui reste entre parenthèses."
                    ),
                )
            )
        else:
            etapes.append(
                Step(
                    "Forme simplifiée",
                    sp.Eq(sp.Symbol(f"f'({variable})"), resultat),
                    explication="On regroupe les termes et on réduit l'écriture "
                    "(mise au même dénominateur, identités usuelles…).",
                )
            )

    for k in range(2, ordre + 1):
        resultat = _forme_reduite(sp.diff(resultat, var))
        nom = "f" + "'" * k
        etapes.append(
            Step(
                f"{nom}({variable}) — dérivée d'ordre {k}",
                sp.Eq(sp.Symbol(nom + f"({variable})"), resultat),
                explication=f"On dérive à nouveau le résultat de l'ordre {k - 1}.",
            )
        )

    return Solution(resultat=resultat, etapes=etapes)
