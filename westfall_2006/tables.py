"""Coefficient and species group tables for Westfall and Laustsen (2006)."""

import csv
from pathlib import Path
from typing import Dict, Tuple

_DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_coefficients() -> Dict[int, Tuple[float, ...]]:
    """Load species group coefficients (β₀–β₇) from CSV."""
    coefficients: Dict[int, Tuple[float, ...]] = {}
    with open(_DATA_DIR / "coefficients.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            group = int(row["Group"])
            betas = tuple(float(row[f"beta_{i}"]) for i in range(8))
            coefficients[group] = betas
    return coefficients


def _load_species_groupings() -> Dict[int, int]:
    """Load FIA species code to group number mapping."""
    mapping: Dict[int, int] = {}
    with open(_DATA_DIR / "species_groupings.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            spcd = int(row["FIA_SPCD"])
            group = int(row["Group no."])
            mapping[spcd] = group
    return mapping


COEFFICIENTS = _load_coefficients()
SPECIES_TO_GROUP = _load_species_groupings()
VALID_GROUPS = set(COEFFICIENTS.keys())
