"""
Models for the Search service API.
"""
from typing import List, Optional, Union

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class FiltersModel(BaseModel):
    """Filters model for product search."""
    freeShipping: Optional[int] = 0
    slug: Optional[str] = "men-shirts"
    vendorIdentifier: Optional[str] = "maskbehrokh"
    maxPrice: Optional[int] = 100000
    minPrice: Optional[int] = 0
    sameCity: Optional[int] = 0
    minRating: Optional[int] = 4
    vendorScore: Optional[int] = 0


class ProductSearchModel(BaseModel):
    """Product search request model."""
    filters: Optional[FiltersModel] = None
    q: Optional[str] = "عسل"
    rows: Optional[int] = 12
    start: Optional[int] = 0
