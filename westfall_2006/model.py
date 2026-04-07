"""Height-to-diameter model from Westfall and Laustsen (2006)."""

import math
from typing import List, Optional, Sequence, Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .tables import (
    COEFFICIENTS,
    GROUP_NAME_TO_NUMBER,
    SPECIES_TO_GROUP,
    VALID_GROUP_NAMES,
    VALID_GROUPS,
)

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


def _resolve_species_group(
    species_group: Optional[Union[int, str, Sequence[str]]] = None,
    fia_spcd: Optional[Union[int, Sequence[int]]] = None,
) -> int:
    """Resolve species_group or fia_spcd input to a single group number.

    Parameters
    ----------
    species_group : int, str, or list of str, optional
        Species group number (1–18) or species group name (e.g. "Poplars").
        If a list of names is provided, all must resolve to the same group.
    fia_spcd : int or list of int, optional
        FIA species code (e.g. 746 for Quaking aspen). If a list is provided,
        all codes must resolve to the same species group.

    Returns
    -------
    int
        The resolved species group number.

    Raises
    ------
    ValueError
        If inputs are invalid or ambiguous.
    """
    if species_group is not None and fia_spcd is not None:
        raise ValueError(
            "Provide either 'species_group' or 'fia_spcd', not both."
        )
    if species_group is None and fia_spcd is None:
        raise ValueError(
            "Must provide either 'species_group' or 'fia_spcd'."
        )

    if species_group is not None:
        if isinstance(species_group, int):
            if species_group not in VALID_GROUPS:
                raise ValueError(
                    f"Invalid species_group {species_group}. "
                    f"Must be between 1 and 18."
                )
            return species_group

        if isinstance(species_group, str):
            key = species_group.strip().lower()
            if key not in GROUP_NAME_TO_NUMBER:
                valid = ", ".join(sorted(VALID_GROUP_NAMES))
                raise ValueError(
                    f"Unknown species group name '{species_group}'. "
                    f"Valid names: {valid}"
                )
            return GROUP_NAME_TO_NUMBER[key]

        # list/sequence of strings
        groups = set()
        for name in species_group:
            key = name.strip().lower()
            if key not in GROUP_NAME_TO_NUMBER:
                valid = ", ".join(sorted(VALID_GROUP_NAMES))
                raise ValueError(
                    f"Unknown species group name '{name}'. "
                    f"Valid names: {valid}"
                )
            groups.add(GROUP_NAME_TO_NUMBER[key])
        if len(groups) != 1:
            raise ValueError(
                f"All species group names must resolve to the same group, "
                f"but got groups: {sorted(groups)}"
            )
        return groups.pop()

    # fia_spcd path
    if isinstance(fia_spcd, int):
        if fia_spcd not in SPECIES_TO_GROUP:
            raise ValueError(
                f"Unknown FIA species code {fia_spcd}. "
                f"Valid codes: {sorted(SPECIES_TO_GROUP.keys())}"
            )
        return SPECIES_TO_GROUP[fia_spcd]

    # list/sequence of ints
    groups = set()
    for code in fia_spcd:
        if code not in SPECIES_TO_GROUP:
            raise ValueError(
                f"Unknown FIA species code {code}. "
                f"Valid codes: {sorted(SPECIES_TO_GROUP.keys())}"
            )
        groups.add(SPECIES_TO_GROUP[code])
    if len(groups) != 1:
        raise ValueError(
            f"All FIA species codes must belong to the same species group, "
            f"but got groups: {sorted(groups)}"
        )
    return groups.pop()


def predict_height_westfall(
    species_group: Optional[Union[int, str, Sequence[str]]] = None,
    dbh_in: Union[float, ArrayLike] = None,
    ccr_pct: Union[float, ArrayLike] = None,
    tree_class: str = None,
    crown_class: str = None,
    top_diam_in: Union[float, ArrayLike] = 0.0,
    *,
    fia_spcd: Optional[Union[int, Sequence[int]]] = None,
) -> Union[float, NDArray]:
    """Predict tree height (ft) at a given top diameter.

    Implements the Chapman-Richards model from Westfall and Laustsen (2006)
    for 18 species groups in Maine.

    Parameters
    ----------
    species_group : int, str, or list of str, optional
        Species group number (1–18), species group name (e.g. "Poplars"),
        or a list of species group names that all belong to the same group.
        Must provide either this or ``fia_spcd``.
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
    fia_spcd : int or list of int, optional (keyword-only)
        FIA species code (e.g. 746 for Quaking aspen), or a list of codes
        that all belong to the same species group. Must provide either this
        or ``species_group``.

    Returns
    -------
    float or numpy.ndarray
        Predicted height in feet.
    """
    resolved_group = _resolve_species_group(species_group, fia_spcd)

    b = COEFFICIENTS[resolved_group]
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
