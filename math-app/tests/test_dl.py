import pytest
import sympy as sp

from solvers.analyse.dl import developpement_limite

x = sp.Symbol("x")


def test_dl_exp_ordre_3():
    sol = developpement_limite("exp(x)", point="0", ordre=3)
    attendu = 1 + x + x**2 / 2 + x**3 / 6
    assert sp.simplify(sol.resultat.removeO() - attendu) == 0


def test_dl_sinus_ordre_5():
    sol = developpement_limite("sin(x)", point="0", ordre=5)
    attendu = x - x**3 / 6 + x**5 / 120
    assert sp.simplify(sol.resultat.removeO() - attendu) == 0


def test_dl_autour_dun_point_non_nul():
    sol = developpement_limite("log(x)", point="1", ordre=2)
    attendu = (x - 1) - (x - 1) ** 2 / 2
    assert sp.simplify(sol.resultat.removeO() - attendu) == 0


def test_ordre_invalide():
    with pytest.raises(ValueError):
        developpement_limite("exp(x)", ordre=0)
