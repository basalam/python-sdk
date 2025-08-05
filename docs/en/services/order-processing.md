# Order Processing Service

Manage customer orders, vendor parcels, and the entire order lifecycle with the Order Processing Service. This service
provides comprehensive functionality to get and manage customer orders, track order items and details, handle vendor
parcels and shipping, generate order statistics, and monitor order status and updates.

## Table of Contents

- [Order Processing Methods](#order-processing-methods)
- [Examples](#examples)

## Order Processing Methods

| Method                                               | Description          | Parameters                                                                                 |
|------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------|
| [`get_customer_orders()`](#get-orders)               | Get orders           | `filters` (OrderFilter)                                                                    |
| [`get_customer_order()`](#get-order)                 | Get specific order   | `order_id`                                                                                 |
| [`get_customer_order_items()`](#get-order-items)     | Get order items      | `filters` (ItemFilter)                                                                     |
| [`get_customer_order_item()`](#get-order-item)       | Get specific item    | `item_id`                                                                                  |
| [`get_vendor_orders_parcels()`](#get-orders-parcels) | Get orders parcels   | `filters` (OrderParcelFilter)                                                              |
| [`get_order_parcel()`](#get-order-parcel)            | Get specific parcel  | `parcel_id`                                                                                |
| [`get_orders_stats()`](#get-order-stats)             | Get order statistics | `resource_count`, `vendor_id`, `product_id`, `customer_id`, `coupon_code`, `cache_control` |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken
from basalam_sdk.order_processing.models import (
    OrderFilter, ItemFilter, OrderParcelFilter, ResourceStats
)

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Get Orders

```python
async def get_customer_orders_example():
    orders = await client.get_customer_orders(
        filters=OrderFilter(
            coupon_code="SAVE10",
            cursor="next_cursor_123",
            customer_ids="123,456,789",
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

### Get Order

```python
async def get_order_example():
    order = await client.get_order(
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
            vendor_ids="456,789"
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
            statuses=[3739, 3237, 3238]  # ParcelStatus enum values
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

## Order Statuses

Common order statuses include:

- `pending` - Order is pending
- `confirmed` - Order is confirmed
- `processing` - Order is being processed
- `shipped` - Order has been shipped
- `delivered` - Order has been delivered
- `cancelled` - Order was cancelled
- `refunded` - Order was refunded

## Parcel Statuses

Common parcel statuses include:

- `pending` - Parcel is pending
- `preparing` - Parcel is being prepared
- `shipped` - Parcel has been shipped
- `in_transit` - Parcel is in transit
- `delivered` - Parcel has been delivered
- `returned` - Parcel was returned

## Next Steps

- [Core Service](./core.md) - Manage vendors, products, and users 
