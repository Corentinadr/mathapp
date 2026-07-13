import pytest

from core import suggestions
from core.parser import parse

_TOUTES = (
    suggestions.DERIVEE
    + suggestions.PRIMITIVE
    + suggestions.INTEGRALE
    + suggestions.LIMITE
    + suggestions.LIMITE_POINTS
    + suggestions.DL
)


@pytest.mark.parametrize("expression", _TOUTES)
def test_suggestion_parsable(expression: str):
    parse(expression)  # ne doit pas lever
