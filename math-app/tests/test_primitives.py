import sympy as sp

from solvers.analyse.primitives import primitiver

x = sp.Symbol("x")
C = sp.Symbol("C")


def test_primitive_polynome():
    sol = primitiver("3x^2 + 2x - 5")
    attendu = x**3 + x**2 - 5 * x + C
    assert sp.simplify(sol.resultat - attendu) == 0


def test_primitive_cosinus():
    sol = primitiver("cos(x)")
    assert sp.simplify(sol.resultat - (sp.sin(x) + C)) == 0


def test_primitive_derivee_recompose_fonction():
    """Vérifie que F'(x) redonne bien f(x)."""
    sol = primitiver("exp(x) * x")
    F_sans_C = sol.resultat - C
    assert sp.simplify(sp.diff(F_sans_C, x) - sp.exp(x) * x) == 0
