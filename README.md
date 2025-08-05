# Basalam Python SDK

## Introduction

Welcome to the Basalam Python SDK - a comprehensive client library for interacting with Basalam API services. This SDK
provides a clean, developer-friendly interface for all Basalam services with full async support. Whether you're building
a server-to-server integration or a user-facing application, this SDK provides the tools you need.

**Supported Python Versions:** Python 3.9+, Python 3.10+, Python 3.11+, Python 3.12+

**Key Features:**

- **Full Async/Sync Support**: All operations support both synchronous and asynchronous patterns
- **Type Safety**: Built with Pydantic for robust type checking and validation
- **Multiple Authentication Methods**: Support for client credentials, authorization code flow, and personal tokens
- **Comprehensive Service Coverage**: Access to all Basalam services including wallet, orders, chat, and more
- **Error Handling**: Detailed error classes for different types of failures
- **Developer Friendly**: Clean API design with comprehensive documentation

![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Services](#services)
    - [Core Service](#core-service)
    - [Chat Service](#chat-service)
    - [Order Service](#order-service)
    - [Order Processing Service](#order-processing-service)
    - [Wallet Service](#wallet-service)
    - [Search Service](#search-service)
    - [Upload Service](#upload-service)
    - [Webhook Service](#webhook-service)
- [Async/Sync Usage](#asyncsync-usage)
- [License](#license)

## Installation

**📖 [Full Introduction Documentation](docs/en/intro.md)**

Install the SDK using pip:

```bash
pip install basalam-sdk
```

## Quick Start

### 1. Import the SDK

```python
from basalam_sdk import BasalamClient, PersonalToken
```

### 2. Set up Authentication

```python
# Personal Token (Token-based authentication)
auth = PersonalToken(
    token="your-access-token",
    refresh_token="your-refresh-token"
)
```

### 3. Create the Client

```python
client = BasalamClient(auth=auth)
```

### 4. Your First API Calls

```python
import asyncio


async def main():
    # Setup
    auth = PersonalToken(
        token="your-access-token",
        refresh_token="your-refresh-token"
    )
    client = BasalamClient(auth=auth)

    # Get products
    products = await client.get_products()
    print(f"Found {len(products)} products")

    # Print first few products
    for product in products[:3]:
        print(f"Product: {product.name} - Price: {product.price}")

    return products


# Run the async function
result = asyncio.run(main())
```

## Authentication

**📖 [Full Authentication Documentation](docs/en/auth.md)**

The SDK supports three main authentication methods:

### Personal Token (For Existing Tokens)

Use this method when you already have valid access and refresh tokens:

```python
from basalam_sdk import BasalamClient, PersonalToken

auth = PersonalToken(
    token="your_existing_access_token",
    refresh_token="your_existing_refresh_token"
)

client = BasalamClient(auth=auth)
```

### Authorization Code Flow (For User Authentication)

Use this method when you need to authenticate on behalf of a user:

```python
from basalam_sdk import BasalamClient, AuthorizationCode, Scope

# Create auth object
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=[Scope.CUSTOMER_WALLET_READ, Scope.CUSTOMER_ORDER_READ]
)

# Get authorization URL
auth_url = auth.get_authorization_url(state="optional_state_parameter")
print(f"Visit: {auth_url}")

# Exchange code for tokens (after user authorization)
token_info = await auth.get_token(code="authorization_code_from_callback")

# Create authenticated client
client = BasalamClient(auth=auth)
```

### Client Credentials (For Server-to-Server)

Use this method for server-to-server applications:

```python
from basalam_sdk import BasalamClient, ClientCredentials, Scope

auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=[Scope.CUSTOMER_WALLET_READ, Scope.VENDOR_PRODUCT_WRITE]
)

client = BasalamClient(auth=auth)
```

## Services

The SDK provides access to all Basalam services through a unified client interface. All services support both
synchronous and asynchronous operations.

### Core Service

**📖 [Full Core Service Documentation](docs/en/services/core.md)**

Manage vendors, products, shipping methods, user information, and more with the Core Service. This service provides
comprehensive functionality for handling core business entities and operations: create and manage vendors, handle
product creation and updates (with file upload support), manage shipping methods, update user verification and
information, handle bank account operations, and manage categories and attributes.

**Key Features:**

- Create and manage vendors
- Handle product creation and updates with file upload support
- Manage shipping methods
- Update user verification and information
- Handle bank account operations
- Manage categories and attributes

**Core Methods:**

| Method                                             | Description                                    | Parameters                                                                 |
|----------------------------------------------------|------------------------------------------------|----------------------------------------------------------------------------|
| `create_vendor()`                                  | Create new vendor                              | `user_id`, `request: CreateVendorSchema`                                   |
| `update_vendor()`                                  | Update vendor                                  | `vendor_id`, `request: UpdateVendorSchema`                                 |
| `get_vendor()`                                     | Get vendor details                             | `vendor_id`, `prefer`                                                      |
| `get_default_shipping_methods()`                   | Get default shipping methods                   | `None`                                                                     |
| `get_shipping_methods()`                           | Get shipping methods                           | `ids`, `vendor_ids`, `include_deleted`, `page`, `per_page`                 |
| `get_working_shipping_methods()`                   | Get working shipping methods                   | `vendor_id`                                                                |
| `update_shipping_methods()`                        | Update shipping methods                        | `vendor_id`, `request: UpdateShippingMethodSchema`                         |
| `get_vendor_products()`                            | Get vendor products                            | `vendor_id`, `query_params: GetVendorProductsSchema`                       |
| `update_vendor_status()`                           | Update vendor status                           | `vendor_id`, `request: UpdateVendorStatusSchema`                           |
| `create_vendor_mobile_change_request()`            | Create vendor mobile change                    | `vendor_id`, `request: ChangeVendorMobileRequestSchema`                    |
| `create_vendor_mobile_change_confirmation()`       | Confirm vendor mobile change                   | `vendor_id`, `request: ChangeVendorMobileConfirmSchema`                    |
| `create_product()`                                 | Create a new product (supports file upload)    | `vendor_id`, `request: ProductRequestSchema`, `photo_files`, `video_file`  |
| `update_bulk_products()`                           | Update multiple products                       | `vendor_id`, `request: BatchUpdateProductsRequest`                         |
| `update_product()`                                 | Update a single product (supports file upload) | `product_id`, `request: ProductRequestSchema`, `photo_files`, `video_file` |
| `get_product()`                                    | Get product details                            | `product_id`, `prefer`                                                     |
| `get_products()`                                   | Get products list                              | `query_params: GetProductsQuerySchema`, `prefer`                           |
| `create_products_bulk_action_request()`            | Create bulk product updates                    | `vendor_id`, `request: BulkProductsUpdateRequestSchema`                    |
| `update_product_variation()`                       | Update product variation                       | `product_id`, `variation_id`, `request: UpdateProductVariationSchema`      |
| `get_products_bulk_action_requests()`              | Get bulk update status                         | `vendor_id`, `page`, `per_page`                                            |
| `get_products_bulk_action_requests_count()`        | Get bulk updates count                         | `vendor_id`                                                                |
| `get_products_unsuccessful_bulk_action_requests()` | Get failed updates                             | `request_id`, `page`, `per_page`                                           |
| `get_product_shelves()`                            | Get product shelves                            | `product_id`                                                               |
| `create_discount()`                                | Create discount for products                   | `vendor_id`, `request: CreateDiscountRequestSchema`                        |
| `delete_discount()`                                | Delete discount for products                   | `vendor_id`, `request: DeleteDiscountRequestSchema`                        |
| `get_current_user()`                               | Get current user info                          | `None`                                                                     |
| `create_user_mobile_confirmation_request()`        | Create mobile confirmation request             | `user_id`                                                                  |
| `verify_user_mobile_confirmation_request()`        | Confirm user mobile                            | `user_id`, `request: ConfirmCurrentUserMobileConfirmSchema`                |
| `create_user_mobile_change_request()`              | Create mobile change request                   | `user_id`, `request: ChangeUserMobileRequestSchema`                        |
| `verify_user_mobile_change_request()`              | Confirm mobile change                          | `user_id`, `request: ChangeUserMobileConfirmSchema`                        |
| `get_user_bank_accounts()`                         | Get user bank accounts                         | `user_id`, `prefer`                                                        |
| `create_user_bank_account()`                       | Create user bank account                       | `user_id`, `request: UserCardsSchema`, `prefer`                            |
| `verify_user_bank_account_otp()`                   | Verify bank account OTP                        | `user_id`, `request: UserCardsOtpSchema`                                   |
| `verify_user_bank_account()`                       | Verify bank accounts                           | `user_id`, `request: UserVerifyBankInformationSchema`                      |
| `delete_user_bank_account()`                       | Delete bank account                            | `user_id`, `bank_account_id`                                               |
| `update_user_bank_account()`                       | Update bank account                            | `bank_account_id`, `request: UpdateUserBankInformationSchema`              |
| `update_user_verification()`                       | Update user verification                       | `user_id`, `request: UserVerificationSchema`                               |
| `get_category_attributes()`                        | Get category attributes                        | `category_id`, `product_id`, `vendor_id`, `exclude_multi_selects`          |
| `get_categories()`                                 | Get all categories                             | `None`                                                                     |
| `get_category()`                                   | Get specific category                          | `category_id`                                                              |

**Example:**

```python
from basalam_sdk.core.models import CreateVendorSchema

# Create a new vendor
vendor = await client.create_vendor(
    user_id=123,
    request=CreateVendorSchema(
        title="My Store",
        identifier="store123",
        category_type=1,
        city=1,
        summary="A great store for all your needs"
    )
)

# Get vendor details
vendor_details = await client.get_vendor(vendor_id=vendor.id)
```

### Chat Service

**📖 [Full Chat Service Documentation](docs/en/services/chat.md)**

Handle messaging and chat functionalities with the Chat Service. This service provides comprehensive tools for managing
conversations, messages, and chat interactions.

**Key Features:**

- Create and manage chat conversations
- Send and retrieve messages
- Handle different message types
- Manage chat participants
- Track chat history and updates

**Methods:**

| Method             | Description       | Parameters                                                                                           |
|--------------------|-------------------|------------------------------------------------------------------------------------------------------|
| `create_message()` | Create a message  | `request`, `user_agent`, `x_client_info`, `admin_token`                                              |
| `create_chat()`    | Create a chat     | `request`, `x_creation_tags`, `x_user_session`, `x_client_info`                                      |
| `get_messages()`   | Get chat messages | `chat_id`, `msg_id`, `limit`, `chat_type`, `order`, `op`, `temp_id`                                  |
| `get_chats()`      | Get chats list    | `limit`, `order_by`, `updated_from`, `updated_before`, `modified_from`, `modified_before`, `filters` |

**Example:**

```python
from basalam_sdk.chat.models import MessageRequest

# Create a message
message = await client.create_message(
    request=MessageRequest(
        chat_id=123,
        content="Hello, how can I help you?",
        message_type="text"
    ),
    user_agent="MyApp/1.0",
    x_client_info="web"
)

# Get messages from a chat
messages = await client.get_messages(
    chat_id=123,
    limit=20,
    order="DESC"
)
```

### Order Service

**📖 [Full Order Service Documentation](docs/en/services/order.md)**

Manage baskets, payments, and invoices with the Order Service. This service provides comprehensive functionality for
handling order-related operations and payment processing.

**Key Features:**

- Manage shopping baskets
- Process payments and invoices
- Handle payment callbacks
- Track order status and product variations
- Manage payable and unpaid invoices

**Methods:**

| Method                           | Description                  | Parameters                                         |
|----------------------------------|------------------------------|----------------------------------------------------|
| `get_baskets()`                  | Get active baskets           | `refresh`                                          |
| `get_product_variation_status()` | Get product variation status | `product_id`                                       |
| `create_invoice_payment()`       | Create payment for invoice   | `invoice_id`, `request`                            |
| `get_payable_invoices()`         | Get payable invoices         | `page`, `per_page`                                 |
| `get_unpaid_invoices()`          | Get unpaid invoices          | `invoice_id`, `status`, `page`, `per_page`, `sort` |
| `get_payment_callback()`         | Get payment callback         | `payment_id`, `request`                            |
| `create_payment_callback()`      | Create payment callback      | `payment_id`, `request`                            |

**Example:**

```python
from basalam_sdk.order.models import CreatePaymentRequestModel

# Get active baskets
baskets = await client.get_baskets(refresh=True)

# Create payment for invoice
payment = await client.create_invoice_payment(
    invoice_id=123,
    request=CreatePaymentRequestModel(
        payment_method="credit_card",
        amount=10000
    )
)
```

### Order Processing Service

**📖 [Full Order Processing Service Documentation](docs/en/services/order-processing.md)**

Manage customer orders, vendor parcels, and the entire order lifecycle with the Order Processing Service. This service
provides comprehensive functionality to get and manage customer orders, track order items and details, handle vendor
parcels and shipping, generate order statistics, and monitor order status and updates.

**Key Features:**

- Get and manage customer orders
- Track order items and details
- Handle vendor parcels and shipping
- Generate order statistics
- Monitor order status and updates

**Methods:**

| Method                        | Description          | Parameters                                                                                 |
|-------------------------------|----------------------|--------------------------------------------------------------------------------------------|
| `get_customer_orders()`       | Get orders           | `filters` (OrderFilter)                                                                    |
| `get_customer_order()`        | Get specific order   | `order_id`                                                                                 |
| `get_customer_order_items()`  | Get order items      | `filters` (ItemFilter)                                                                     |
| `get_customer_order_item()`   | Get specific item    | `item_id`                                                                                  |
| `get_vendor_orders_parcels()` | Get orders parcels   | `filters` (OrderParcelFilter)                                                              |
| `get_order_parcel()`          | Get specific parcel  | `parcel_id`                                                                                |
| `get_orders_stats()`          | Get order statistics | `resource_count`, `vendor_id`, `product_id`, `customer_id`, `coupon_code`, `cache_control` |

**Example:**

```python
from basalam_sdk.order_processing.models import OrderFilter

# Get orders with filters
orders = await client.get_customer_orders(
    filters=OrderFilter(
        coupon_code="SAVE10",
        cursor="next_cursor_123",
        customer_ids="123,456,789",
        customer_name="John Doe"
    )
)

# Get specific order details
order = await client.get_customer_order(order_id=123)
```

### Wallet Service

**📖 [Full Wallet Service Documentation](docs/en/services/wallet.md)**

Manage user balances, expenses, and refunds with the Wallet Service. This service provides comprehensive functionality
for handling user financial operations.

**Key Features:**

- Get user balance and transaction history
- Create and manage expenses
- Process refunds
- Handle credit-specific operations

**Methods:**

| Method                         | Description                         | Parameters                                                                    |
|--------------------------------|-------------------------------------|-------------------------------------------------------------------------------|
| `get_balance()`                | Get user's balance                  | `user_id`, `filters`, `x_operator_id`                                         |
| `get_transactions()`           | Get transaction history             | `user_id`, `page`, `per_page`, `x_operator_id`                                |
| `create_expense()`             | Create an expense                   | `user_id`, `request`, `x_operator_id`                                         |
| `create_expense_from_credit()` | Create expense from specific credit | `user_id`, `credit_id`, `request`, `x_operator_id`                            |
| `get_expense()`                | Get expense details                 | `user_id`, `expense_id`, `x_operator_id`                                      |
| `delete_expense()`             | Delete/rollback expense             | `user_id`, `expense_id`, `rollback_reason_id`, `x_operator_id`                |
| `get_expense_by_ref()`         | Get expense by reference            | `user_id`, `reason_id`, `reference_id`, `x_operator_id`                       |
| `delete_expense_by_ref()`      | Delete expense by reference         | `user_id`, `reason_id`, `reference_id`, `rollback_reason_id`, `x_operator_id` |
| `create_refund()`              | Process a refund                    | `request`, `x_operator_id`                                                    |
| `can_rollback_refund()`        | Check if refund can be rolled back  | `refund_reason`, `refund_reference_id`, `x_operator_id`                       |
| `rollback_refund()`            | Rollback a refund                   | `request`, `x_operator_id`                                                    |

**Example:**

```python
from basalam_sdk.wallet.models import SpendCreditRequest

# Get user balance
balance = await client.get_balance(user_id=123)

# Create an expense
expense = await client.create_expense(
    user_id=123,
    request=SpendCreditRequest(
        reason_id=1,
        reference_id=456,
        amount=10000,
        description="Payment for order #456",
        types=[1, 2],
        settleable=True
    )
)
```

### Search Service

**📖 [Full Search Service Documentation](docs/en/services/search.md)**

Search for products and entities with the Search Service. This service provides powerful search capabilities.

**Key Features:**

- Search for products with advanced filters
- Apply price ranges and category filters
- Sort results by various criteria
- Paginate through search results
- Get detailed product information

**Methods:**

| Method              | Description         | Parameters |
|---------------------|---------------------|------------|
| `search_products()` | Search for products | `request`  |

**Example:**

```python
from basalam_sdk.search.models import ProductSearchModel

# Search for products
results = await client.search_products(
    request=ProductSearchModel(
        query="laptop",
        category_id=123,
        min_price=100000,
        max_price=500000,
        sort_by="price",
        sort_order="asc",
        page=1,
        per_page=20
    )
)
```

### Upload Service

**📖 [Full Upload Service Documentation](docs/en/services/upload.md)**

Upload and manage files with the Upload Service. This service provides secure file upload capabilities.

**Key Features:**

- Upload files securely
- Support various file types (images, documents, videos)
- Set custom file names and expiration times
- Get file URLs for access
- Manage file lifecycle

**Methods:**

| Method          | Description   | Parameters                                                  |
|-----------------|---------------|-------------------------------------------------------------|
| `upload_file()` | Upload a file | `file`, `file_type`, `custom_unique_name`, `expire_minutes` |

**Example:**

```python
from basalam_sdk.upload.models import UserUploadFileTypeEnum

# Upload a file
with open("image.jpg", "rb") as file:
    result = await client.upload_file(
        file=file,
        file_type=UserUploadFileTypeEnum.PRODUCT_PHOTO,
        custom_unique_name="my-product-image",
        expire_minutes=1440  # 24 hours
    )

    print(f"File uploaded: {result.url}")
```

### Webhook Service

**📖 [Full Webhook Service Documentation](docs/en/services/webhook.md)**

Manage webhook subscriptions and events with the Webhook Service. This service allows you to receive real-time
notifications about events happening in your Basalam account.

**Key Features:**

- Create and manage webhook subscriptions
- Handle different types of events
- Monitor webhook logs and delivery status
- Register and unregister clients to webhooks

**Methods:**

| Method                      | Description                | Parameters                       |
|-----------------------------|----------------------------|----------------------------------|
| `get_webhook_services()`    | Get webhook services       | None                             |
| `create_webhook_service()`  | Create webhook service     | `request`                        |
| `get_webhooks()`            | Get webhooks list          | `service_id`, `event_ids`        |
| `create_webhook()`          | Create new webhook         | `request`                        |
| `update_webhook()`          | Update webhook             | `webhook_id`, `request`          |
| `delete_webhook()`          | Delete webhook             | `webhook_id`                     |
| `get_webhook_events()`      | Get available events       | None                             |
| `get_webhook_customers()`   | Get webhook customers      | `page`, `per_page`, `webhook_id` |
| `get_webhook_logs()`        | Get webhook logs           | `webhook_id`                     |
| `register_webhook()`        | Register client to webhook | `request`                        |
| `unregister_webhook()`      | Unregister client          | `request`                        |
| `get_registered_webhooks()` | Get registered webhooks    | `page`, `per_page`, `service_id` |

**Example:**

```python
from basalam_sdk.webhook.models import CreateWebhookRequest

# Create a new webhook
webhook = await client.create_webhook(
    request=CreateWebhookRequest(
        service_id=1,
        event_ids=["order.created", "payment.completed"],
        request_method="POST",
        url="https://your-app.com/webhook",
        is_active=True
    )
)

# Get webhook events
events = await client.get_webhook_events()
```

## Async/Sync Usage

All SDK methods support both synchronous and asynchronous patterns:

### Asynchronous (Recommended)

```python
async def async_example():
    auth = PersonalToken(token="your-token", refresh_token="your-refresh-token")
    client = BasalamClient(auth=auth)

    # Async calls
    balance = await client.get_balance(user_id=123)
    webhooks = await client.get_webhooks()

    return balance, webhooks


# Run async function
result = asyncio.run(async_example())
```

### Synchronous

```python
def sync_example():
    auth = PersonalToken(token="your-token", refresh_token="your-refresh-token")
    client = BasalamClient(auth=auth)

    # Sync calls (note the _sync suffix)
    balance = client.get_balance_sync(user_id=123)
    webhooks = client.get_webhooks_sync()

    return balance, webhooks
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
