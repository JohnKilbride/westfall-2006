"""Westfall and Laustsen (2006) merchantable and total height model."""

from .model import predict_height_westfall
from .tables import GROUP_NAME_TO_NUMBER, SPECIES_TO_GROUP

__all__ = [
    "predict_height_westfall",
    "SPECIES_TO_GROUP",
    "GROUP_NAME_TO_NUMBER",
]
