from typing import Protocol

from core.types import Solution


class Solveur(Protocol):
    """Interface commune : reçoit une expression + paramètres, retourne une Solution."""

    def __call__(self, expression: str, **parametres) -> Solution: ...
