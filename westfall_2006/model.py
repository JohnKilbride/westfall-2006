"""Height-to-diameter model from Westfall and Laustsen (2006)."""

import math
from typing import Optional, Sequence, Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .tables import COEFFICIENTS, SPECIES_TO_GROUP, VALID_GROUPS

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


def _fia_spcd_to_species_group(
    fia_spcd: Union[int, ArrayLike],
) -> Union[int, NDArray]:
    """Convert FIA species code(s) to species group number(s).

    Parameters
    ----------
    fia_spcd : int or array_like of int
        FIA species code(s) to convert.

    Returns
    -------
    int or numpy.ndarray
        Corresponding species group number(s).

    Raises
    ------
    ValueError
        If any code is not recognised.
    """
    if isinstance(fia_spcd, int):
        if fia_spcd not in SPECIES_TO_GROUP:
            raise ValueError(
                f"Unknown FIA species code {fia_spcd}. "
                f"Valid codes: {sorted(SPECIES_TO_GROUP.keys())}"
            )
        return SPECIES_TO_GROUP[fia_spcd]

    arr = np.asarray(fia_spcd)
    unknown = [int(c) for c in arr.flat if int(c) not in SPECIES_TO_GROUP]
    if unknown:
        raise ValueError(
            f"Unknown FIA species code(s) {unknown}. "
            f"Valid codes: {sorted(SPECIES_TO_GROUP.keys())}"
        )
    return np.vectorize(SPECIES_TO_GROUP.__getitem__)(arr)


def _validate_inputs(
    species_group: Union[int, ArrayLike],
    dbh_in: Union[float, ArrayLike],
    ccr_pct: Union[float, ArrayLike],
    top_diam_in: Union[float, ArrayLike],
) -> None:
    """Validate numeric inputs to predict_height_westfall.

    Checks that species_group values are recognised, dbh_in is positive,
    ccr_pct is in [0, 100], and top_diam_in is non-negative.  String
    inputs (tree_class and crown_class) are validated implicitly by their
    respective encoding functions.

    Raises
    ------
    ValueError
        If any input fails a range or validity check.
    """
    # --- species_group ---
    sg_arr = np.asarray(species_group)
    invalid_sg = [int(g) for g in sg_arr.flat if int(g) not in VALID_GROUPS]
    if invalid_sg:
        raise ValueError(
            f"Invalid species_group(s) {invalid_sg}. Must be between 1 and 18."
        )

    # --- dbh_in ---
    dbh_arr = np.asarray(dbh_in, dtype=float)
    if np.any(dbh_arr <= 0):
        raise ValueError("dbh_in must be positive (> 0).")

    # --- ccr_pct ---
    ccr_arr = np.asarray(ccr_pct, dtype=float)
    if np.any((ccr_arr < 0) | (ccr_arr > 100)):
        raise ValueError("ccr_pct must be in [0, 100].")

    # --- top_diam_in ---
    top_arr = np.asarray(top_diam_in, dtype=float)
    if np.any(top_arr < 0):
        raise ValueError("top_diam_in must be non-negative (>= 0).")


def predict_height_westfall(
    species_group: Optional[Union[int, ArrayLike]],
    dbh_in: Union[float, ArrayLike],
    ccr_pct: Union[float, ArrayLike],
    tree_class: Union[str, ArrayLike],
    crown_class: Union[str, ArrayLike],
    top_diam_in: Union[float, ArrayLike] = 0.0,
    *,
    fia_spcd: Optional[Union[int, ArrayLike]] = None,
) -> Union[float, NDArray]:
    """Predict tree height (ft) at a given top diameter.

    Implements the Chapman-Richards model from Westfall and Laustsen (2006)
    for 18 species groups in Maine.

    All six parameters accept either a scalar value or an array-like, enabling
    vectorized prediction over mixed-species, mixed-class stands in a single
    call. When any parameter is array-like, all parameters are broadcast
    together and a NumPy array is returned; otherwise a single float is
    returned.

    Parameters
    ----------
    species_group : int or array_like of int
        Species group number (1–18).  This is the primary way to specify the
        species.  Pass ``None`` only when supplying ``fia_spcd`` instead.
    dbh_in : float or array_like
        Diameter at breast height (inches, > 0).
    ccr_pct : float or array_like
        Compacted crown ratio (percent, 0–100).
    tree_class : str or array_like of str
        Tree class: "preferred", "acceptable", "rough", "rotten", or "dead".
    crown_class : str or array_like of str
        Crown class: "dead", "intermediate", "dominant", "codominant",
        "open grown", or "overtopped".
    top_diam_in : float or array_like, optional
        Top diameter (inches, >= 0) at which to predict height. Default is 0,
        which gives total tree height.
    fia_spcd : int or array_like of int, optional (keyword-only)
        FIA species code(s) (e.g. 746 for Quaking aspen) as an alternative to
        ``species_group``.  Converted to species group numbers before
        prediction.  Mutually exclusive with ``species_group``.

    Returns
    -------
    float or numpy.ndarray
        Predicted height in feet.

    Raises
    ------
    ValueError
        If neither or both of ``species_group`` and ``fia_spcd`` are provided,
        or if any input fails a range/validity check.
    """
    # Resolve species_group from fia_spcd when needed.
    if species_group is None and fia_spcd is None:
        raise ValueError("Either species_group or fia_spcd must be provided.")
    if species_group is not None and fia_spcd is not None:
        raise ValueError(
            "Provide either species_group or fia_spcd, not both."
        )
    if fia_spcd is not None:
        species_group = _fia_spcd_to_species_group(fia_spcd)

    _validate_inputs(species_group, dbh_in, ccr_pct, top_diam_in)

    is_array = any(
        isinstance(v, (list, np.ndarray))
        for v in (species_group, dbh_in, ccr_pct, tree_class, crown_class, top_diam_in)
    )

    if not is_array:
        b = COEFFICIENTS[species_group]
        cc1, cc2, cc3 = _encode_crown_class(crown_class)
        tc = _encode_tree_class(tree_class)
        asymptote = b[0] * top_diam_in + b[1] * cc1 + b[2] * cc2 + b[3] * cc3
        base = 1.0 - math.exp(-b[4] * dbh_in)
        exponent = b[5] * ccr_pct + b[6] * tc + pow(top_diam_in / dbh_in + 0.01, b[7])
        return asymptote * pow(base, exponent)

    # Array path: convert all inputs
    sg = np.asarray(species_group)
    dbh_in = np.asarray(dbh_in, dtype=float)
    ccr_pct = np.asarray(ccr_pct, dtype=float)
    top_diam_in = np.asarray(top_diam_in, dtype=float)

    # Build coefficient arrays indexed by species group.
    # Result shape: (8,) when sg is 0-d, (*sg.shape, 8) when sg is n-d.
    b_rows = [COEFFICIENTS[int(g)] for g in sg.flat]
    if sg.ndim == 0:
        b_mat = np.array(b_rows[0], dtype=float)        # shape (8,)
    else:
        b_mat = np.array(b_rows, dtype=float).reshape(*sg.shape, 8)

    b0, b1, b2, b3, b4, b5, b6, b7 = (b_mat[..., i] for i in range(8))

    # Encode tree_class (scalar string or array of strings)
    tc = np.frompyfunc(_encode_tree_class, 1, 1)(np.asarray(tree_class)).astype(float)

    # Encode crown_class (scalar string or array of strings)
    cc1, cc2, cc3 = np.frompyfunc(_encode_crown_class, 1, 3)(np.asarray(crown_class))
    cc1, cc2, cc3 = cc1.astype(float), cc2.astype(float), cc3.astype(float)

    # Chapman-Richards computation
    asymptote = b0 * top_diam_in + b1 * cc1 + b2 * cc2 + b3 * cc3
    base = 1.0 - np.exp(-b4 * dbh_in)
    exponent = b5 * ccr_pct + b6 * tc + np.power(top_diam_in / dbh_in + 0.01, b7)
    return asymptote * np.power(base, exponent)
