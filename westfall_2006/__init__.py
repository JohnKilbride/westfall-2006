"""Westfall and Laustsen (2006) merchantable and total height model."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("westfall-2006")
except PackageNotFoundError:
    __version__ = "unknown"

from .model import predict_height_westfall
from .tables import SPECIES_TO_GROUP

__all__ = [
    "predict_height_westfall",
    "SPECIES_TO_GROUP",
]
