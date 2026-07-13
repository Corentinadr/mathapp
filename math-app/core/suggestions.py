"""Suggestions proposées dans les champs de saisie des exercices.

Chaque liste est testée (tests/test_suggestions.py) : toute suggestion doit être
parsable par core.parser.parse.
"""

DERIVEE = [
    "x^3 - 2x^2 + 5x - 7",
    "sin(x) * cos(x)",
    "x^2 * exp(x)",
    "log(x) / x",
    "sqrt(1 + x^2)",
    "tan(x)",
    "arctan(x)",
    "1 / (1 + x^2)",
]

PRIMITIVE = [
    "3x^2 + 2x - 5",
    "cos(x)",
    "x * exp(x)",
    "1 / (1 + x^2)",
    "1 / x",
    "sin(x)^2",
    "1 / sqrt(1 - x^2)",
    "tan(x)",
]

INTEGRALE = [
    "x^2",
    "sin(x)",
    "exp(-x^2)",
    "1 / (1 + x^2)",
    "x * log(x)",
    "sqrt(x)",
    "cos(x)^2",
    "x * exp(-x)",
]

LIMITE = [
    "sin(x) / x",
    "(1 - cos(x)) / x^2",
    "(exp(x) - 1) / x",
    "(1 + 1/x)^x",
    "log(1 + x) / x",
    "tan(x) / x",
    "x * log(x)",
    "1 / x",
]

LIMITE_POINTS = ["0", "oo", "-oo", "1", "pi"]

DL = [
    "exp(x)",
    "sin(x)",
    "cos(x)",
    "log(1 + x)",
    "1 / (1 - x)",
    "sqrt(1 + x)",
    "tan(x)",
    "arctan(x)",
]
