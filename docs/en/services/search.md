# Search Service

Search for products and entities with the Search Service. This service provides powerful search capabilities: search for
products with advanced filters, apply price ranges and category filters, sort results by various criteria, paginate
through search results, and get detailed product information.

## Table of Contents

- [Search Methods](#search-methods)
- [Examples](#examples)

## Search Methods

### Methods

| Method                                          | Description         | Parameters |
|-------------------------------------------------|---------------------|------------|
| [`search_products()`](#search-products-example) | Search for products | `request`  |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.search.models import ProductSearchModel, FiltersModel

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Search Products Example

```python
async def search_products_example():
    results = await client.search_products(
        request=ProductSearchModel(
            filters=FiltersModel(
                freeShipping=1,
                slug="electronics",
                vendorIdentifier="vendor123",
                maxPrice=500000,
                minPrice=100000,
                sameCity=1,
                minRating=4,
                vendorScore=80
            ),
            q="laptop",
            rows=20,
            start=0
        )
    )
    
    print(f"Search results: {results}")
    return results
