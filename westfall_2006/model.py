"""Height-to-diameter model from Westfall and Laustsen (2006)."""

import math
from typing import Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .tables import COEFFICIENTS, VALID_GROUPS

CROWN_CLASS_ENCODING = {
    "intermediate": (1, 0, 0),
    "dead": (1, 0, 0),
    "dominant": (0, 1, 0),
    "codominant": (0, 1, 0),
    "open grown": (0, 1, 0),
    "overtopped": (0, 0, 1),
}

TREE_CLASS_ENCODING = {
    "preferred": 1,
    "acceptable": 2,
    "rough": 3,
    "rotten": 3,
    "dead": 3,
}


def _encode_crown_class(crown_class: str):
    """Convert a crown class string to one-hot encoded (CC1, CC2, CC3)."""
    key = crown_class.strip().lower()
    if key not in CROWN_CLASS_ENCODING:
        valid = ", ".join(sorted(CROWN_CLASS_ENCODING.keys()))
        raise ValueError(
            f"Invalid crown_class '{crown_class}'. Must be one of: {valid}"
        )
    return CROWN_CLASS_ENCODING[key]


def _encode_tree_class(tree_class: str) -> int:
    """Convert a tree class string to its integer code (1–3)."""
    key = tree_class.strip().lower()
    if key not in TREE_CLASS_ENCODING:
        valid = ", ".join(sorted(TREE_CLASS_ENCODING.keys()))
        raise ValueError(
            f"Invalid tree_class '{tree_class}'. Must be one of: {valid}"
        )
    return TREE_CLASS_ENCODING[key]


def predict_height_westfall(
    species_group: int,
    dbh_in: Union[float, ArrayLike],
    ccr_pct: Union[float, ArrayLike],
    tree_class: str,
    crown_class: str,
    top_diam_in: Union[float, ArrayLike] = 0.0,
) -> Union[float, NDArray]:
    """Predict tree height (ft) at a given top diameter.

    Implements the Chapman-Richards model from Westfall and Laustsen (2006)
    for 18 species groups in Maine.

    Parameters
    ----------
    species_group : int
        Species group number (1–18).
    dbh_in : float or array_like
        Diameter at breast height (inches).
    ccr_pct : float or array_like
        Compacted crown ratio (percent, 0–100).
    tree_class : str
        Tree class: "preferred", "acceptable", "rough", "rotten", or "dead".
    crown_class : str
        Crown class: "dead", "intermediate", "dominant", "codominant",
        "open grown", or "overtopped".
    top_diam_in : float or array_like, optional
        Top diameter (inches) at which to predict height. Default is 0,
        which gives total tree height.

    Returns
    -------
    float or numpy.ndarray
        Predicted height in feet.
    """
    if species_group not in VALID_GROUPS:
        raise ValueError(
            f"Invalid species_group {species_group}. Must be between 1 and 18."
        )

    b = COEFFICIENTS[species_group]
    cc1, cc2, cc3 = _encode_crown_class(crown_class)
    tc = _encode_tree_class(tree_class)

    is_array = any(isinstance(v, (list, np.ndarray)) for v in (dbh_in, ccr_pct, top_diam_in))

    if is_array:
        dbh_in = np.asarray(dbh_in, dtype=float)
        ccr_pct = np.asarray(ccr_pct, dtype=float)
        top_diam_in = np.asarray(top_diam_in, dtype=float)
        exp = np.exp
        power = np.power
    else:
        exp = math.exp
        power = pow

    # Asymptote term
    asymptote = b[0] * top_diam_in + b[1] * cc1 + b[2] * cc2 + b[3] * cc3

    # Chapman-Richards base
    base = 1.0 - exp(-b[4] * dbh_in)

    # Shape exponent
    exponent = b[5] * ccr_pct + b[6] * tc + power(top_diam_in / dbh_in + 0.01, b[7])

    return asymptote * power(base, exponent)
