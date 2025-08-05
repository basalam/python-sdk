"""
Models for the Search service API.
"""
from typing import Optional

from pydantic import BaseModel


class FiltersModel(BaseModel):
    """Filters model for product search."""
    freeShipping: Optional[int] = None
    slug: Optional[str] = None
    vendorIdentifier: Optional[str] = None
    maxPrice: Optional[int] = None
    minPrice: Optional[int] = None
    sameCity: Optional[int] = None
    minRating: Optional[int] = None
    vendorScore: Optional[int] = None


class ProductSearchModel(BaseModel):
    """Product search request model."""
    filters: Optional[FiltersModel] = None
    q: Optional[str] = None
    rows: Optional[int] = None
    start: Optional[int] = None
