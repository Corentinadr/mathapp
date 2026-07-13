import pytest
import sympy as sp

from solvers.analyse.derivees import deriver

x = sp.Symbol("x")


def test_derivee_polynome():
    sol = deriver("x^3 - 2x^2 + 5x - 7")
    assert sp.simplify(sol.resultat - (3 * x**2 - 4 * x + 5)) == 0


def test_derivee_seconde():
    sol = deriver("x^3", ordre=2)
    assert sp.simplify(sol.resultat - 6 * x) == 0


def test_derivee_sinus():
    sol = deriver("sin(x)")
    assert sp.simplify(sol.resultat - sp.cos(x)) == 0


def test_ordre_invalide():
    with pytest.raises(ValueError):
        deriver("x^2", ordre=0)


def _titres(sol):
    return [e.title for e in sol.etapes]


def test_regle_du_produit_nommee():
    sol = deriver("x^2 * sin(x)")
    assert any("produit" in t.lower() for t in _titres(sol))
    assert sp.simplify(sol.resultat - (2 * x * sp.sin(x) + x**2 * sp.cos(x))) == 0


def test_regle_du_quotient_nommee():
    sol = deriver("log(x) / x")
    assert any("quotient" in t.lower() for t in _titres(sol))
    assert sp.simplify(sol.resultat - (1 - sp.log(x)) / x**2) == 0


def test_regle_de_la_chaine_nommee():
    sol = deriver("sin(2x)")
    assert any("chaîne" in t.lower() for t in _titres(sol))
    assert sp.simplify(sol.resultat - 2 * sp.cos(2 * x)) == 0


def test_linearite_nommee():
    sol = deriver("x^2 + sin(x)")
    assert any("linéarité" in t.lower() for t in _titres(sol))


def test_e_puissance_x_sans_log_et_factorise():
    """(x²·eˣ)' doit donner (x² + 2x)eˣ sans artefact log(e), avec l'étape de factorisation."""
    sol = deriver("x^2 * e^x")
    assert not sol.resultat.has(sp.log)
    assert sp.simplify(sol.resultat - (x**2 + 2 * x) * sp.exp(x)) == 0
    etape_facto = next(e for e in sol.etapes if e.title == "Factorisation")
    assert "facteur commun" in etape_facto.explication
