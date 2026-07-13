import pytest

from core.generateur import TYPES, generer, resoudre


@pytest.mark.parametrize("type_exercice", TYPES)
def test_exercices_generes_solvables(type_exercice: str):
    """Chaque type généré doit être résoluble sans erreur (10 tirages)."""
    for _ in range(10):
        exo = generer(type_exercice)
        assert exo["latex"]
        assert exo["consigne"]
        solution = resoudre(exo)
        assert solution.resultat is not None
        assert solution.etapes


def test_type_inconnu_leve_erreur():
    with pytest.raises(ValueError):
        generer("geometrie")
