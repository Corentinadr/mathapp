from dataclasses import dataclass, field
from typing import Any

import sympy as sp


@dataclass
class Step:
    title: str
    expression: sp.Expr | sp.Equality | str
    explication: str = ""


@dataclass
class Exercise:
    enonce: str
    parametres: dict[str, Any] = field(default_factory=dict)


@dataclass
class Solution:
    resultat: sp.Expr | sp.Equality | list | str
    etapes: list[Step] = field(default_factory=list)
