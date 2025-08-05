"""
Tests for the Search service client.
"""
import pytest

from basalam_sdk import BasalamClient
from basalam_sdk.auth import PersonalToken
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.search.models import ProductSearchModel, FiltersModel


@pytest.fixture
def basalam_client():
    """Create a BasalamClient instance with real auth and config."""
    config = BasalamConfig(
        environment=Environment.PRODUCTION,
        timeout=30.0,
        user_agent="SDK-Test"
    )
    auth = PersonalToken(
        token=""
    )
    return BasalamClient(auth=auth, config=config)


@pytest.mark.asyncio
async def test_search_products_async(basalam_client):
    """Test searching products asynchronously."""
    # Create search request
    search_request = ProductSearchModel(
        q="سیب",
        filters=FiltersModel(
            maxPrice=100000,
            minPrice=10000,
            minRating=4
        )
    )

    # Call the method
    result = await basalam_client.search_products(search_request)

    # Print the result
    print(f"Async search result: {result}")

    # Check response
    assert isinstance(result, dict)
    assert result is not None


def test_search_products_sync(basalam_client):
    """Test searching products synchronously."""
    # Create search request
    search_request = ProductSearchModel(
        q="laptop",
        rows=10,
        start=0,
        filters=FiltersModel(
            maxPrice=100000,
            minPrice=10000,
            minRating=4
        )
    )

    # Call the method
    result = basalam_client.search_products_sync(search_request)

    # Print the result
    print(f"Sync search result: {result}")

    # Check response
    assert isinstance(result, dict)
    assert result is not None
