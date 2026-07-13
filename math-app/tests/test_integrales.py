import sympy as sp

from solvers.analyse.integrales import integrer


def test_integrale_polynome():
    sol = integrer("x^2", "0", "1")
    assert sol.resultat == sp.Rational(1, 3)


def test_integrale_sinus():
    sol = integrer("sin(x)", "0", "pi")
    assert sol.resultat == 2


def test_integrale_gaussienne_sur_R():
    sol = integrer("exp(-x^2)", "-oo", "oo")
    assert sp.simplify(sol.resultat - sp.sqrt(sp.pi)) == 0
