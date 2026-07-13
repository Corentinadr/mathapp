import sympy as sp

from core.parser import parse

x = sp.Symbol("x")


def test_parse_expression_simple():
    expr = parse("2x^2 + 3x - 5")
    assert str(expr) == "2*x**2 + 3*x - 5"


def test_parse_notations_francaises():
    assert parse("arctan(x)") == sp.atan(x)
    assert parse("arcsin(x)") == sp.asin(x)
    assert parse("ch(x)^2 - sh(x)^2") == sp.cosh(x) ** 2 - sp.sinh(x) ** 2


def test_parse_e_est_la_constante_euler():
    assert parse("e^x") == sp.exp(x)
    assert parse("e") == sp.E
