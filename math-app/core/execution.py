"""Exécution des solveurs : cache de résultats + délai maximal.

Le timeout utilise un thread : à l'expiration on rend la main à l'UI avec une
erreur claire ; le calcul abandonné se termine en arrière-plan (un thread Python
ne peut pas être tué). Le pool est borné pour éviter l'accumulation.
"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as _Timeout
from typing import Any, Callable

import streamlit as st

DELAI_DEFAUT = 15.0

_pool = ThreadPoolExecutor(max_workers=2)


class CalculTropLong(Exception):
    """Le calcul formel dépasse le délai autorisé."""


@st.cache_data(show_spinner=False, max_entries=200)
def _calcul_en_cache(_fn: Callable, cle: str, args: tuple, kwargs_tries: tuple, delai: float) -> Any:
    future = _pool.submit(_fn, *args, **dict(kwargs_tries))
    try:
        return future.result(timeout=delai)
    except _Timeout:
        raise CalculTropLong(
            f"Le calcul a dépassé {delai:.0f} secondes et a été abandonné. "
            "Essaie une expression plus simple ou des bornes finies."
        ) from None


def calculer(fn: Callable, *args: Any, _delai: float = DELAI_DEFAUT, **kwargs: Any) -> Any:
    """Exécute un solveur avec cache et timeout.

    `cle` identifie la fonction dans la clé de cache (le paramètre `_fn` lui-même
    est exclu du hachage par convention Streamlit — préfixe underscore).
    """
    cle = f"{fn.__module__}.{fn.__qualname__}"
    return _calcul_en_cache(fn, cle, args, tuple(sorted(kwargs.items())), _delai)
