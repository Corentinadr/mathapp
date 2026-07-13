import pytest
import sympy as sp

from solvers.algebre.equations import resoudre_second_degre


def test_deux_racines_reelles():
    sol = resoudre_second_degre(1, -3, 2)
    assert sorted(sol.resultat) == [1, 2]
    assert len(sol.etapes) == 5


def test_racine_double():
    sol = resoudre_second_degre(1, -2, 1)
    assert sol.resultat == [1]
    assert len(sol.etapes) == 4


def test_racines_complexes():
    sol = resoudre_second_degre(1, 0, 1)
    assert set(sol.resultat) == {sp.I, -sp.I}


def test_a_nul_leve_erreur():
    with pytest.raises(ValueError):
        resoudre_second_degre(0, 2, 1)
