import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)

# Notations françaises / usuelles → objets SymPy
_NOTATIONS = {
    "e": sp.E,  # sinon « e^x » devient un symbole quelconque et (e^x)' traîne un log(e)
    "arctan": sp.atan,
    "arcsin": sp.asin,
    "arccos": sp.acos,
    "argsh": sp.asinh,
    "argch": sp.acosh,
    "argth": sp.atanh,
    "sh": sp.sinh,
    "ch": sp.cosh,
    "th": sp.tanh,
}


def parse(expression: str) -> sp.Expr:
    """Parse une expression mathématique saisie par l'utilisateur (ex: '2x^2 + 3x - 5')."""
    normalisee = expression.replace("^", "**")
    return parse_expr(normalisee, transformations=_TRANSFORMATIONS, local_dict=_NOTATIONS)
