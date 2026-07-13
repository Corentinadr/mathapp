import pytest
import sympy as sp

from solvers.analyse.limites import calculer_limite


def test_limite_sinus_sur_x_en_0():
    sol = calculer_limite("sin(x)/x", "0")
    assert sol.resultat == 1


def test_limite_infinie():
    sol = calculer_limite("1/x^2", "0")
    assert sol.resultat == sp.oo


def test_limite_a_l_infini():
    sol = calculer_limite("(1+1/x)^x", "oo")
    assert sol.resultat == sp.E


def test_limite_gauche_vs_droite():
    sol_g = calculer_limite("1/x", "0", direction="à gauche")
    sol_d = calculer_limite("1/x", "0", direction="à droite")
    assert sol_g.resultat == -sp.oo
    assert sol_d.resultat == sp.oo


def test_direction_invalide():
    with pytest.raises(ValueError):
        calculer_limite("x", "0", direction="au milieu")


def test_etape_forme_indeterminee_reste_une_equation():
    """Eq(f(0), nan) ne doit pas s'auto-évaluer en False (rendu LaTeX cassé sinon)."""
    sol = calculer_limite("sin(x)/x", "0")
    etape_substitution = sol.etapes[2]
    assert etape_substitution.expression is not sp.false
    assert isinstance(etape_substitution.expression, sp.Eq)
