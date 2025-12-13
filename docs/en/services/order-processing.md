# Order Processing Service

Manage customer orders, vendor parcels, and the entire order lifecycle with the Order Processing Service. This service
provides comprehensive functionality to get and manage customer orders, track order items and details, handle vendor
parcels and shipping, generate order statistics, and monitor order status and updates.

## Table of Contents

- [Order Processing Methods](#order-processing-methods)
- [Examples](#examples)
- [Parcel Status Codes](#parcel-status-codes)
- [Shipping Method Codes](#shipping-method-codes)

## Order Processing Methods

| Method                                                            | Description                      | Parameters                                                                                 |
|-------------------------------------------------------------------|----------------------------------|--------------------------------------------------------------------------------------------|
| [`get_customer_orders()`](#get-customer-orders)                   | Get orders                       | `filters` (OrderFilter)                                                                    |
| [`get_customer_order()`](#get-customer-order)                     | Get specific order               | `order_id`                                                                                 |
| [`get_customer_order_parcel_hints()`](#get-order-parcel-hints)    | Get order parcel hints           | `order_id`                                                                                 |
| [`get_customer_order_items()`](#get-order-items)                  | Get order items                  | `filters` (ItemFilter)                                                                     |
| [`get_customer_order_item()`](#get-order-item)                    | Get specific item                | `item_id`                                                                                  |
| [`get_vendor_orders_parcels()`](#get-vendor-orders-parcels)       | Get vendor orders parcels        | `filters` (OrderParcelFilter)                                                              |
| [`get_order_parcel()`](#get-order-parcel)                         | Get specific parcel              | `parcel_id`                                                                                |
| [`set_order_parcel_preparation()`](#set-order-parcel-preparation) | Mark parcel as in preparation    | `parcel_id`                                                                                |
| [`set_order_parcel_posted()`](#set-order-parcel-posted)           | Mark parcel as posted/shipped    | `parcel_id`, `posted_data` (PostedOrderRequest)                                            |
| [`get_orders_stats()`](#get-order-stats)                          | Get order statistics             | `resource_count`, `vendor_id`, `product_id`, `customer_id`, `coupon_code`, `cache_control` |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.order_processing.models import (
    ItemFilter,
    OrderFilter,
    OrderParcelFilter,
    ParcelStatus,
    PostedOrderRequest,
    ResourceStats,
    ShippingMethodCode,
)

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Get Customer Orders

```python
async def get_customer_orders_example():
    orders = await client.get_customer_orders(
        filters=OrderFilter(
            coupon_code="SAVE10",
            cursor="next_cursor_123",
            customer_ids=["123", "456", "789"],
            customer_name="John Doe",
            ids="1,2,3",
            items_title="laptop",
            paid_at="2024-01-01",
            parcel_estimate_send_at="2024-01-15",
            parcel_statuses=["posted", "delivered"],
            per_page=20,
            product_ids="1,2,3",
            sort="paid_at:desc",
            vendor_ids="456,789"
        )
    )

    return orders
```

### Get Customer Order

```python
async def get_customer_order_example():
    order = await client.get_customer_order(
        order_id=123
    )

    return order
```

### Get Order Items

```python
async def get_customer_order_items_example():
    items = await client.get_customer_order_items(
        filters=ItemFilter(
            created_at="2024-01-01",
            cursor="next_cursor_123",
            customer_ids="123,456,789",
            ids="1,2,3",
            order_ids="1,2,3",
            per_page=20,
            product_ids="1,2,3",
            sort="created_at:desc",
            vendor_ids=["456", "789"]
        )
    )

    return items
```

### Get Order Item

```python
async def get_customer_order_item_example():
    item = await client.get_customer_order_item(
        item_id=456
    )

    return item
```

### Get Order Parcel Hints

```python
async def get_customer_order_parcel_hints_example():
    hints = await client.get_customer_order_parcel_hints(
        order_id=123
    )

    return hints
```

### Get Orders Parcels

```python
async def get_vendor_orders_parcels_example():
    parcels = await client.get_vendor_orders_parcels(
        filters=OrderParcelFilter(
            created_at="2024-01-01",
            cursor="next_cursor_123",
            estimate_send_at="2024-01-15",
            ids="1,2,3",
            items_customer_ids="123,456,789",
            items_order_ids="1,2,3",
            items_product_ids=["1", "2", "3"],
            items_vendor_ids=["456", "789"],
            per_page=20,
            sort="estimate_send_at:desc",
            statuses=[
                ParcelStatus.NEW_ORDER,
                ParcelStatus.PREPARATION_IN_PROGRESS,
            ]
        )
    )

    return parcels
```

### Get Order Parcel

```python
async def get_order_parcel_example():
    parcel = await client.get_order_parcel(
        parcel_id=789
    )

    return parcel
```

### Set Order Parcel Preparation

```python
async def set_order_parcel_preparation_example():
    result = await client.set_order_parcel_preparation(parcel_id=789)
    return result
```

### Set Order Parcel Posted

```python
async def set_order_parcel_posted_example():
    result = await client.set_order_parcel_posted(
        parcel_id=789,
        posted_data=PostedOrderRequest(
            tracking_code="IR1234567890",
            shipping_method=ShippingMethodCode.EXPRESS,
        )
    )
    return result
```

### Get Order Stats

```python
async def get_orders_stats_example():
    stats = await client.get_orders_stats(
        resource_count=ResourceStats.NUMBER_OF_ORDERS_PER_VENDOR,
        vendor_id=456,
        product_id=123,
        customer_id=789,
        coupon_code="SAVE10",
        cache_control="no-cache"
    )

    return stats
```

## Parcel Status Codes

- `NEW_ORDER` (3739)
- `PREPARATION_IN_PROGRESS` (3237)
- `POSTED` (3238)
- `WRONG_TRACKING_CODE` (5017)
- `PRODUCT_IS_NOT_DELIVERED` (3572)
- `PROBLEM_IS_REPORTED` (3740)
- `CUSTOMER_CANCEL_REQUEST_FROM_CUSTOMER` (4633)
- `OVERDUE_AGREEMENT_REQUEST_FROM_VENDOR` (5075)
- `SATISFIED` (3195)
- `DEFINITIVE_DISSATISFACTION` (3233)
- `CANCEL` (3067)

## Shipping Method Codes

- `SPECIAL` (3197)
- `EXPRESS` (3198)
- `COURIER` (3259)
- `TRANSIT` (5137)
- `TIPAX` (4040)
- `MAHEX` (6102)
- `CHAPAR` (6101)
- `AMADAST` (6110)
- `DECA` (6111)
- `CHEETA` (6112)
- `BOXIT` (6113)
- `SALAM_RESAN` (6114)

## Next Steps

- [Core Service](./core.md) - Manage vendors, products, and users 
