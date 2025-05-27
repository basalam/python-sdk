# Basalam SDK Usage Guide

This document provides a comprehensive guide on how to use the Basalam SDK effectively. It covers installation,
configuration, authentication, and usage examples for the various services provided by the SDK.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Authentication](#authentication)
4. [Basic Usage](#basic-usage)
5. [Service-Specific Usage](#service-specific-usage)
    - [Webhook Service](#webhook-service)
    - [Wallet Service](#wallet-service)
    - [Order Processing Service](#order-processing-service)
    - [Upload Service](#upload-service)
    - [Search Service](#search-service)
6. [Error Handling](#error-handling)
7. [Advanced Usage](#advanced-usage)

## Installation

Install the SDK using pip:

```bash
pip install basalam-sdk
```

## Configuration

The SDK uses the `BasalamConfig` class for configuration and can be configured programmatically:

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials
from basalam_sdk.config import BasalamConfig

# Create a configuration object
config = BasalamConfig(
    api_base_url="https://api.example.com",
    api_version="v1",
    timeout=30
)

# Create authentication with this config
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    config=config
)

# Create client with auth and config
client = BasalamClient(auth=auth, config=config)
```

You can customize various configuration parameters:

| Parameter      | Description                 | Default                        |
|----------------|-----------------------------|--------------------------------|
| `api_base_url` | Base URL of the Basalam API | `https://api.basalam.com`      |
| `api_version`  | API version to use          | `v1`                           |
| `timeout`      | Request timeout in seconds  | `30`                           |
| `user_agent`   | User Agent string           | `Basalam-Python-SDK/{version}` |

## Authentication

The SDK supports multiple authentication methods:

### Client Credentials

For server-to-server authentication:

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials

# Create authentication object
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=["webhook:read", "wallet:read"]
)

# Create a client with this authentication
client = BasalamClient(auth=auth)

# Use the authenticated client
webhooks = client.webhook.get_webhooks_sync()
```

### Authorization Code

For user-specific authentication:

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import AuthorizationCode

# Create an authorization object
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=["webhook:read", "webhook:write"]
)

# Get the authorization URL
auth_url = auth.get_authorization_url(state="random-state-value")

# Redirect user to auth_url
# After authorization, exchange the code for a token
token_info = auth.exchange_code_sync("authorization_code_from_callback")

# Create client with the auth object
client = BasalamClient(auth=auth)
```

### Token Management

The SDK automatically manages tokens including refreshing them when needed:

```python
# Token info is accessible through the auth object
token_info = auth.token_info
if token_info and token_info.is_expired:
    print("Token has expired")

# Manually refresh a token if needed
client.refresh_auth_token_sync()
```

## Basic Usage

### Creating a Client

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials

# Create authentication
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Create a client
client = BasalamClient(auth=auth)

# Access services
webhooks = client.webhook.get_webhooks_sync()
balance = client.wallet.get_balance_sync()
```

### Async vs Sync Methods

The SDK provides both asynchronous and synchronous methods:

```python
# Synchronous usage
webhooks = client.webhook.get_webhooks_sync()

# Asynchronous usage
import asyncio

async def get_webhooks_async():
    webhooks = await client.webhook.get_webhooks()
    return webhooks

# Run the async function
webhooks = asyncio.run(get_webhooks_async())
```

## Service-Specific Usage

### Webhook Service

The Webhook Service allows you to manage webhooks for event notifications.

#### Listing Webhooks

```python
# Synchronous
webhooks = client.webhook.get_webhooks_sync()
print(f"Found {webhooks.result_count} webhooks")

# Asynchronous
async def list_webhooks():
    webhooks = await client.webhook.get_webhooks()
    print(f"Found {webhooks.result_count} webhooks")
    
    for webhook in webhooks.data:
        print(f"Webhook ID: {webhook.id}, URL: {webhook.url}")
```

#### Creating Webhooks

```python
from basalam_sdk.webhook import CreateWebhookRequest

# Create a request model
webhook_request = CreateWebhookRequest(
    event_ids=[1, 2, 3],
    request_method="POST",
    url="https://my-service.com/webhook",
    is_active=True
)

# Create the webhook
webhook = client.webhook.create_webhook_sync(webhook_request)
print(f"Created webhook with ID: {webhook.id}")
```

#### Updating Webhooks

```python
from basalam_sdk.webhook import UpdateWebhookRequest

# Create an update request
update_request = UpdateWebhookRequest(
    url="https://my-service.com/webhook/v2",
    is_active=True
)

# Update the webhook
webhook = client.webhook.update_webhook_sync(
    webhook_id=123,
    request=update_request
)
```

#### Deleting Webhooks

```python
# Delete a webhook
response = client.webhook.delete_webhook_sync(webhook_id=123)
print(f"Webhook {response.id} deleted at {response.deleted_at}")
```

### Wallet Service

The Wallet Service provides access to wallet operations.

#### Getting Wallet Balance

```python
# Get wallet balance
balance = client.wallet.get_balance_sync()
print(f"Current balance: {balance.amount} {balance.currency}")
```

#### Creating a Transaction

```python
from basalam_sdk.wallet import CreateTransactionRequest

# Create a transaction request
transaction_request = CreateTransactionRequest(
    amount=100.50,
    currency="USD",
    description="Payment for Order #12345"
)

# Create the transaction
transaction = client.wallet.create_transaction_sync(transaction_request)
print(f"Transaction ID: {transaction.id}, Status: {transaction.status}")
```

### Order Processing Service

The Order Processing Service allows management of orders.

#### Getting Orders

```python
# Get a list of orders
orders = client.order_processing.get_orders_sync(
    page=1,
    per_page=20,
    status="pending"
)

print(f"Found {orders.total_count} orders, showing {len(orders.data)}")

for order in orders.data:
    print(f"Order #{order.id}: {order.status}, Amount: {order.total_amount}")
```

#### Creating an Order

```python
from basalam_sdk.order_processing import CreateOrderRequest, OrderItem

# Create order items
items = [
    OrderItem(product_id=123, quantity=2, price=25.99),
    OrderItem(product_id=456, quantity=1, price=15.50)
]

# Create order request
order_request = CreateOrderRequest(
    customer_id=789,
    items=items,
    shipping_address_id=101,
    payment_method="credit_card"
)

# Create the order
order = client.order_processing.create_order_sync(order_request)
print(f"Created Order #{order.id}")
```

### Upload Service

The Upload Service handles file uploads.

#### Uploading a File

```python
from basalam_sdk.upload import UserUploadFileTypeEnum

# Upload a file
with open("image.jpg", "rb") as file:
    response = client.upload.create_file_sync(
        file=file,
        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
        custom_unique_name="product-123-main"
    )

print(f"File uploaded: {response.file_name}")
print(f"URL: {response.url}")
```

### Search Service

The Search Service provides product search capabilities.

#### Searching for Products

```python
from basalam_sdk.search import ProductSearchModel, FiltersModel

# Create search filters
filters = FiltersModel(
    min_price=10.0,
    max_price=100.0,
    free_shipping=True
)

# Create search request
search_request = ProductSearchModel(
    q="organic honey",
    filters=filters,
    rows=25,
    start=0
)

# Search for products
results = client.search.search_products_sync(search_request)

print(f"Found {len(results.products)} products")
for product in results.products:
    print(f"Product: {product.title}, Price: {product.price}")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from basalam_sdk.errors import (
    BasalamApiError, BasalamAuthError, 
    ResourceNotFoundError, ValidationError, 
    RateLimitError
)

try:
    webhook = client.webhook.get_webhook_sync(webhook_id=999)
except ResourceNotFoundError as e:
    print(f"Webhook not found: {e}")
except ValidationError as e:
    print(f"Validation error: {e.errors}")
except BasalamAuthError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except BasalamApiError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Advanced Usage

### Custom HTTP Headers

```python
# Add custom headers to a specific request
webhooks = client.webhook.get_webhooks_sync(
    headers={
        "X-Custom-Header": "value",
        "X-Tracking-ID": "request-123"
    }
)

# Set default headers for all requests from a client
client = BasalamClient(
    auth=auth,
    default_headers={
        "X-Application-Name": "MyApp",
        "X-Application-Version": "1.0.0"
    }
)
```

### Request Timeout Control

```python
# Set timeout for a specific request (in seconds)
try:
    webhooks = client.webhook.get_webhooks_sync(timeout=5)
except BasalamApiError as e:
    if "timeout" in str(e).lower():
        print("Request timed out")
    else:
        raise
```

### Using Proxy Servers

```python
from basalam_sdk.config import BasalamConfig

# Configure proxy in the config
config = BasalamConfig(
    proxies={
        "http": "http://proxy.example.com:8080",
        "https": "https://proxy.example.com:8080"
    }
)

# Create client with this config
client = BasalamClient(auth=auth, config=config)
```

### Debugging Requests

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# The SDK will now output detailed request/response information
```

This comprehensive guide covers the core functionality of the Basalam SDK. For more detailed information about specific
services and advanced features, refer to the service-specific documentation or the API reference. 
