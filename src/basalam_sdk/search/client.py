"""
Client for the Search service API.

This module provides a client for interacting with Basalam's search service.
"""

import logging
from typing import Dict, Any

from .models import ProductSearchModel
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class SearchService(BaseClient):
    """Client for the Search service API."""

    def __init__(self, **kwargs):
        """Initialize the search service client."""
        super().__init__(service="search", **kwargs)

    async def search_products(self, request: ProductSearchModel) -> Dict[str, Any]:
        """
        Search for products.
        
        Args:
            request: The search request model containing filters and search parameters.
            
        Returns:
            The search results.
        """
        endpoint = "/v1/products/search"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), require_auth=False)
        return response

    def search_products_sync(self, request: ProductSearchModel) -> Dict[str, Any]:
        """
        Search for products (synchronous version).
        
        Args:
            request: The search request model containing filters and search parameters.
            
        Returns:
            The search results.
        """
        endpoint = "/v1/products/search"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), require_auth=False)
        return response
