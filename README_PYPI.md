# Basalam Python SDK

[![Python Version](https://img.shields.io/pypi/pyversions/basalam-sdk)](https://pypi.org/project/basalam-sdk/)
[![PyPI Version](https://img.shields.io/pypi/v/basalam-sdk)](https://pypi.org/project/basalam-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python SDK for interacting with Basalam API services. This SDK provides a clean, developer-friendly interface for all Basalam services with full async/sync support.

## Features

- **Full Async/Sync Support**: All operations support both synchronous and asynchronous patterns
- **Type Safety**: Built with Pydantic for robust type checking and validation  
- **Multiple Authentication Methods**: Support for client credentials, authorization code flow, and personal tokens
- **Comprehensive Service Coverage**: Access to all Basalam services including wallet, orders, chat, and more
- **Auto-retry Logic**: Built-in retry mechanisms for better reliability
- **Detailed Error Handling**: Specific error classes for different failure scenarios

## Installation

```bash
pip install basalam-sdk
```

## Quick Start

```python
from basalam_sdk import BasalamClient, PersonalToken
import asyncio

async def main():
    # Initialize with your credentials
    auth = PersonalToken(
        token="your-access-token",
        refresh_token="your-refresh-token"
    )
    client = BasalamClient(auth=auth)
    
    # Get products
    products = await client.get_products()
    print(f"Found {len(products)} products")
    
    # Get user balance
    balance = await client.get_balance(user_id=123)
    print(f"Balance: {balance}")

# Run async
asyncio.run(main())
```

## Authentication

The SDK supports three authentication methods:

### Personal Token
```python
from basalam_sdk import PersonalToken

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
```

### Client Credentials (Server-to-Server)
```python
from basalam_sdk import ClientCredentials, Scope

auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=[Scope.CUSTOMER_CHAT_READ]
)
```

### Authorization Code (OAuth2 Flow)
```python
from basalam_sdk import AuthorizationCode, Scope

auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=[Scope.CUSTOMER_ORDER_READ]
)

# Get authorization URL
auth_url = auth.get_authorization_url()
# After user authorization, exchange code for tokens
token_info = await auth.get_token(code="received_code")
```

## Available Services

### Core Service
Manage vendors, products, shipping methods, and user information.

```python
# Create a vendor
vendor = await client.create_vendor(
    user_id=123,
    request=CreateVendorSchema(
        title="My Store",
        summary="store123"
    )
)

# Create a product with images
product = await client.create_product(
    vendor_id=456,
    request=ProductRequestSchema(
        name="Sample Product",
        price=100000
    ),
    photo_files=[("photo1.jpg", photo_bytes)]
)
```

### Wallet Service
Handle user balances, transactions, and refunds.

```python
# Get balance
balance = await client.get_balance(user_id=123)

# Create expense
expense = await client.create_expense(
    user_id=123,
    request=SpendCreditRequest(
        amount=10000,
        reason_id=1
    )
)
```

### Order Service
Manage shopping baskets and payment processing.

```python
# Get active baskets
baskets = await client.get_baskets(refresh=True)

# Create payment
payment = await client.create_invoice_payment(
    invoice_id=789,
    request=CreatePaymentRequestModel(
        payment_method="credit_card"
    )
)
```

### Chat Service
Handle messaging and conversations.

```python
# Send message
message = await client.create_message(
    request=MessageRequest(
        chat_id=123,
        content="Hello!"
    )
)

# Get messages
messages = await client.get_messages(chat_id=123)
```

### Search Service
Search products with advanced filtering.

```python
# Search products
results = await client.search_products(
    request=ProductSearchModel(
        query="laptop",
        min_price=100000,
        max_price=500000
    )
)
```

### Additional Services
- **Order Processing**: Track orders and parcels
- **Upload**: Secure file uploads  
- **Webhook**: Real-time event notifications

## Sync/Async Usage

All methods support both patterns:

```python
# Async (recommended)
balance = await client.get_balance(user_id=123)

# Sync
balance = client.get_balance_sync(user_id=123)
```

## Documentation

For detailed documentation and examples, visit:
- [GitHub Repository](https://github.com/basalam/python-sdk)
- [Developers Documentation](https://developers.basalam.com/)

## License

MIT License - see [LICENSE](https://github.com/basalam/python-sdk/blob/main/LICENSE) for details.