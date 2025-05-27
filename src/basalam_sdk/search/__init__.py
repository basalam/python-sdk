"""
Search service module for the Basalam SDK.

This module provides access to Basalam's search service APIs.
"""

from .client import SearchService
from .models import ProductSearchModel, FiltersModel

__all__ = [
    "SearchService",
    "ProductSearchModel",
    "FiltersModel",
]
