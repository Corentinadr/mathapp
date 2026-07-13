import time

import pytest

from core.execution import CalculTropLong, calculer
from solvers.analyse.derivees import deriver


def _lent(duree: float) -> str:
    time.sleep(duree)
    return "fini"


def test_calculer_retourne_le_resultat_du_solveur():
    sol = calculer(deriver, "x^2")
    assert str(sol.resultat) == "2*x"


def test_timeout_leve_calcul_trop_long():
    with pytest.raises(CalculTropLong):
        calculer(_lent, 2.0, _delai=0.2)
