# Order Service

Manage baskets, payments, and invoices with the Order Service. This service provides comprehensive functionality for
handling order-related operations and payment processing: manage shopping baskets, process payments and invoices, handle
payment callbacks, track order status and product variations, and manage payable and unpaid invoices.

## Table of Contents

- [Order Methods](#order-methods)
- [Examples](#examples)

## Order Methods

### Methods

| Method                                                                    | Description                  | Parameters                                         |
|---------------------------------------------------------------------------|------------------------------|----------------------------------------------------|
| [`get_baskets()`](#get-baskets-example)                                   | Get active baskets           | `refresh`                                          |
| [`get_product_variation_status()`](#get-product-variation-status-example) | Get product variation status | `product_id`                                       |
| [`create_invoice_payment()`](#create-invoice-payment-example)             | Create payment for invoice   | `invoice_id`, `request`                            |
| [`get_payable_invoices()`](#get-payable-invoices-example)                 | Get payable invoices         | `page`, `per_page`                                 |
| [`get_unpaid_invoices()`](#get-unpaid-invoices-example)                   | Get unpaid invoices          | `invoice_id`, `status`, `page`, `per_page`, `sort` |
| [`get_payment_callback()`](#get-payment-callback-example)                 | Get payment callback         | `payment_id`, `request`                            |
| [`create_payment_callback()`](#create-payment-callback-example)           | Create payment callback      | `payment_id`, `request`                            |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.order.models import (
    CreatePaymentRequestModel, PaymentCallbackRequestModel, PaymentVerifyRequestModel,
    UnpaidInvoiceStatusEnum, OrderEnum
)

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Get Baskets Example

```python
async def get_baskets_example():
    baskets = await client.get_baskets(
        refresh=True
    )

    print(f"Basket ID: {baskets.id}")
    print(f"Item count: {baskets.item_count}")
    print(f"Error count: {baskets.error_count}")

    if baskets.vendors:
        for vendor in baskets.vendors:
            print(f"Vendor: {vendor.title} - Items: {len(vendor.items) if vendor.items else 0}")

    return baskets
```

### Get Product Variation Status Example

```python
async def get_product_variation_status_example():
    status = await client.get_product_variation_status(
        product_id=123
    )

    print(f"Product variation status: {status}")
    return status
```

### Create Invoice Payment Example

```python
async def create_invoice_payment_example():
    payment = await client.create_invoice_payment(
        invoice_id=456,
        request=CreatePaymentRequestModel(
            pay_drivers={
                "gateway": {"amount": 50000},
                "credit": {"amount": 25000},
                "salampay": {"amount": 0},
                "other": {"amount": 0}
            },
            callback="https://example.com/callback",
            option_code="OPTION123",
            national_id="1234567890"
        )
    )

    print(f"Payment created: {payment}")
    return payment
```

### Get Payable Invoices Example

```python
async def get_payable_invoices_example():
    invoices = await client.get_payable_invoices(
        page=1,
        per_page=10
    )

    print(f"Payable invoices: {invoices}")
    return invoices
```

### Get Unpaid Invoices Example

```python
async def get_unpaid_invoices_example():
    invoices = await client.get_unpaid_invoices(
        invoice_id=123,
        status=UnpaidInvoiceStatusEnum.UNPAID,
        page=1,
        per_page=20,
        sort=OrderEnum.DESC
    )

    print(f"Unpaid invoices: {invoices}")
    return invoices
```

### Get Payment Callback Example

```python
async def get_payment_callback_example():
    callback = await client.get_payment_callback(
        payment_id=789,
        request=PaymentCallbackRequestModel(
            status="success",
            transaction_id="txn_123456",
            description="Payment completed successfully"
        )
    )

    print(f"Payment callback: {callback}")
    return callback
```

### Create Payment Callback Example

```python
async def create_payment_callback_example():
    callback = await client.create_payment_callback(
        payment_id=789,
        request=PaymentVerifyRequestModel(
            payment_id="pay_123456",
            transaction_id="txn_123456",
            description="Payment verification completed"
        )
    )

    print(f"Payment callback created: {callback}")
    return callback
```

## Payment Methods

Available payment methods include:

- `credit_card` - Credit card payments
- `debit_card` - Debit card payments
- `bank_transfer` - Bank transfer
- `digital_wallet` - Digital wallet payments
- `cash_on_delivery` - Cash on delivery

## Payment Statuses

Common payment statuses:

- `pending` - Payment is pending
- `success` - Payment completed successfully
- `failed` - Payment failed
- `cancelled` - Payment was cancelled
- `refunded` - Payment was refunded

## Next Steps

- [Upload Service](./upload.md) - File upload and management
- [Search Service](./search.md) - Search for products and entities
- [Order Processing Service](./order-processing.md) - Process orders and parcels 
