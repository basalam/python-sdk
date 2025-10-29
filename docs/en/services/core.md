# Core Service

Manage vendors, products, shipping methods, user information, and more with the Core Service. This service provides
comprehensive functionality for handling core business entities and operations: create and manage vendors, handle
product creation and updates (with file upload support), manage shipping methods, update user verification and
information, handle bank account operations, and manage categories and attributes.

## Table of Contents

- [Core Methods](#core-methods)
- [Examples](#examples)

## Core Methods

| Method                                                                                                | Description                                    | Parameters                                                                 |
|-------------------------------------------------------------------------------------------------------|------------------------------------------------|----------------------------------------------------------------------------|
| [`create_vendor()`](#create-vendor)                                                                   | Create new vendor                              | `user_id`, `request: CreateVendorSchema`                                   |
| [`update_vendor()`](#update-vendor)                                                                   | Update vendor                                  | `vendor_id`, `request: UpdateVendorSchema`                                 |
| [`get_vendor()`](#get-vendor)                                                                         | Get vendor details                             | `vendor_id`, `prefer`                                                      |
| [`get_default_shipping_methods()`](#get-default-shipping-methods)                                     | Get default shipping methods                   | `None`                                                                     |
| [`get_shipping_methods()`](#get-shipping-methods)                                                     | Get shipping methods                           | `ids`, `vendor_ids`, `include_deleted`, `page`, `per_page`                 |
| [`get_working_shipping_methods()`](#get-working-shipping-methods)                                     | Get working shipping methods                   | `vendor_id`                                                                |
| [`update_shipping_methods()`](#update-shipping-methods)                                               | Update shipping methods                        | `vendor_id`, `request: UpdateShippingMethodSchema`                         |
| [`get_vendor_products()`](#get-vendor-products)                                                       | Get vendor products                            | `vendor_id`, `query_params: GetVendorProductsSchema`                       |
| [`update_vendor_status()`](#update-vendor-status)                                                     | Update vendor status                           | `vendor_id`, `request: UpdateVendorStatusSchema`                           |
| [`create_vendor_mobile_change_request()`](#create-vendor-mobile-change-request)                       | Create vendor mobile change                    | `vendor_id`, `request: ChangeVendorMobileRequestSchema`                    |
| [`create_vendor_mobile_change_confirmation()`](#create-vendor-mobile-change-confirmation)             | Confirm vendor mobile change                   | `vendor_id`, `request: ChangeVendorMobileConfirmSchema`                    |
| [`create_product()`](#create-product)                                                                 | Create a new product (supports file upload)    | `vendor_id`, `request: ProductRequestSchema`, `photo_files`, `video_file`  |
| [`update_bulk_products()`](#update-bulk-products)                                                     | Update multiple products                       | `vendor_id`, `request: BatchUpdateProductsRequest`                         |
| [`update_product()`](#update-product)                                                                 | Update a single product (supports file upload) | `product_id`, `request: ProductRequestSchema`, `photo_files`, `video_file` |
| [`get_product()`](#get-product)                                                                       | Get product details                            | `product_id`, `prefer`                                                     |
| [`get_products()`](#get-products)                                                                     | Get products list                              | `query_params: GetProductsQuerySchema`, `prefer`                           |
| [`create_products_bulk_action_request()`](#create-products-bulk-action-request)                       | Create bulk product updates                    | `vendor_id`, `request: BulkProductsUpdateRequestSchema`                    |
| [`update_product_variation()`](#update-product-variation)                                             | Update product variation                       | `product_id`, `variation_id`, `request: UpdateProductVariationSchema`      |
| [`get_products_bulk_action_requests()`](#get-products-bulk-action-requests)                           | Get bulk update status                         | `vendor_id`, `page`, `per_page`                                            |
| [`get_products_bulk_action_requests_count()`](#get-products-bulk-action-requests-count)               | Get bulk updates count                         | `vendor_id`                                                                |
| [`get_products_unsuccessful_bulk_action_requests()`](#get-products-unsuccessful-bulk-action-requests) | Get failed updates                             | `request_id`, `page`, `per_page`                                           |
| [`get_product_shelves()`](#get-product-shelves)                                                       | Get product shelves                            | `product_id`                                                               |
| [`create_discount()`](#create-discount)                                                               | Create discount for products                   | `vendor_id`, `request: CreateDiscountRequestSchema`                        |
| [`delete_discount()`](#delete-discount)                                                               | Delete discount for products                   | `vendor_id`, `request: DeleteDiscountRequestSchema`                        |
| [`get_current_user()`](#get-current-user)                                                             | Get current user info                          | `None`                                                                     |
| [`create_user_mobile_confirmation_request()`](#create-user-mobile-confirmation-request)               | Create mobile confirmation request             | `user_id`                                                                  |
| [`verify_user_mobile_confirmation_request()`](#verify-user-mobile-confirmation-request)               | Confirm user mobile                            | `user_id`, `request: ConfirmCurrentUserMobileConfirmSchema`                |
| [`create_user_mobile_change_request()`](#create-user-mobile-change-request)                           | Create mobile change request                   | `user_id`, `request: ChangeUserMobileRequestSchema`                        |
| [`verify_user_mobile_change_request()`](#verify-user-mobile-change-request)                           | Confirm mobile change                          | `user_id`, `request: ChangeUserMobileConfirmSchema`                        |
| [`get_user_bank_accounts()`](#get-user-bank-accounts)                                                 | Get user bank accounts                         | `user_id`, `prefer`                                                        |
| [`create_user_bank_account()`](#create-user-bank-account)                                             | Create user bank account                       | `user_id`, `request: UserCardsSchema`, `prefer`                            |
| [`verify_user_bank_account_otp()`](#verify-user-bank-account-otp)                                     | Verify bank account OTP                        | `user_id`, `request: UserCardsOtpSchema`                                   |
| [`verify_user_bank_account()`](#verify-user-bank-account)                                             | Verify bank accounts                           | `user_id`, `request: UserVerifyBankInformationSchema`                      |
| [`delete_user_bank_account()`](#delete-user-bank-account)                                             | Delete bank account                            | `user_id`, `bank_account_id`                                               |
| [`update_user_bank_account()`](#update-user-bank-account)                                             | Update bank account                            | `user_id`, `bank_account_id`, `request: UpdateUserBankInformationSchema`   |
| [`update_user_verification()`](#update-user-verification)                                             | Update user verification                       | `user_id`, `request: UserVerificationSchema`                               |
| [`get_category_attributes()`](#get-category-attributes)                                               | Get category attributes                        | `category_id`, `product_id`, `vendor_id`, `exclude_multi_selects`          |
| [`get_categories()`](#get-categories)                                                                 | Get all categories                             | `None`                                                                     |
| [`get_category()`](#get-category)                                                                     | Get specific category                          | `category_id`                                                              |
| [`create_shelve()`](#create-shelve)                                                                   | Create a new shelve                            | `request: ShelveSchema`                                                    |
| [`update_shelve()`](#update-shelve)                                                                   | Update a shelve                                | `shelve_id`, `request: ShelveSchema`                                       |
| [`delete_shelve()`](#delete-shelve)                                                                   | Delete a shelve                                | `shelve_id`                                                                |
| [`get_shelve_products()`](#get-shelve-products)                                                       | Get products in a shelve                       | `shelve_id`, `title`                                                       |
| [`update_shelve_products()`](#update-shelve-products)                                                 | Update products in a shelve                    | `shelve_id`, `request: UpdateShelveProductsSchema`                         |
| [`delete_shelve_product()`](#delete-shelve-product)                                                   | Delete product from shelve                     | `shelve_id`, `product_id`                                                  |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Create Vendor

```python
from basalam_sdk.core.models import CreateVendorSchema


async def create_vendor_example():
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

    return vendor
```

### Update Vendor

```python
from basalam_sdk.core.models import UpdateVendorSchema


async def update_vendor_example():
    updated_vendor = await client.update_vendor(
        vendor_id=456,
        request=UpdateVendorSchema(
            title="Updated Store Name",
            summary="Updated description",
        )
    )

    return updated_vendor
```

### Get Vendor

```python
async def get_vendor_example():
    vendor = await client.get_vendor(
        vendor_id=456,
        prefer="return=minimal"
    )

    return vendor
```

### Get Default Shipping Methods

```python
async def get_default_shipping_methods_example():
    shipping_methods = await client.get_default_shipping_methods()

    return shipping_methods
```

### Get Shipping Methods

```python
async def get_shipping_methods_example():
    shipping_methods = await client.get_shipping_methods()

    return shipping_methods
```

### Get Working Shipping Methods

```python
async def get_working_shipping_methods_example():
    working_methods = await client.get_working_shipping_methods(
        vendor_id=456
    )

    return working_methods
```

### Update Shipping Methods

```python
from basalam_sdk.core.models import UpdateShippingMethodSchema


async def update_shipping_methods_example():
    updated_methods = await client.update_shipping_methods(
        vendor_id=456,
        request=UpdateShippingMethodSchema(
            shipping_methods=[
                {
                    "method_id": 3198,
                    "is_customized": True,
                    "base_cost": 50000
                }
            ]
        )
    )

    return updated_methods
```

### Get Vendor Products

```python
from basalam_sdk.core.models import GetVendorProductsSchema, ProductStatusInputEnum


async def get_vendor_products_example():
    products = await client.get_vendor_products(
        vendor_id=456,
        query_params=GetVendorProductsSchema(
            statuses=[ProductStatusInputEnum.PUBLISHED],
            page=1,
            per_page=10
        )
    )

    return products
```

### Update Vendor Status

```python
from basalam_sdk.core.models import UpdateVendorStatusSchema


async def update_vendor_status_example():
    status_update = await client.update_vendor_status(
        vendor_id=456,
        request=UpdateVendorStatusSchema(
            status=VendorStatusInputEnum.SEMI_ACTIVE,
            description="Vendor is Semi Active"
        )
    )

    return status_update
```

### Create Vendor Mobile Change Request

```python
from basalam_sdk.core.models import ChangeVendorMobileRequestSchema


async def create_vendor_mobile_change_request_example():
    result = await client.create_vendor_mobile_change_request(
        vendor_id=456,
        request=ChangeVendorMobileRequestSchema(
            mobile="09123456789"
        )
    )

    return result
```

### Create Vendor Mobile Change Confirmation

```python
from basalam_sdk.core.models import ChangeVendorMobileConfirmSchema


async def create_vendor_mobile_change_confirmation_example():
    result = await client.create_vendor_mobile_change_confirmation(
        vendor_id=456,
        request=ChangeVendorMobileConfirmSchema(
            mobile="09123456789",
            verification_code=123456
        )
    )

    return result
```

### Create Product

```python
from basalam_sdk.core.models import ProductRequestSchema, ProductStatusInputEnum, UnitTypeInputEnum
import io


async def create_product_example():
    try:
        with open("test1.png", "rb") as photo1,
                open("test2.png", "rb") as photo2:
            request = ProductRequestSchema(
                name="Product 01",
                description="The material of this product is very high quality and made of silk.",
                category_id=238,
                primary_price=100000,
                weight=300,
                package_weight=500,
                stock=10,
                status=ProductStatusInputEnum.PUBLISHED,
                unit_quantity=10,
                unit_type=UnitTypeInputEnum.NUMERIC
            )
            product = await client.core.create_product(456, request, photo_files=[photo1, photo2])

    return product
```

### Update Bulk Products

```python
from basalam_sdk.core.models import BatchUpdateProductsRequest, UpdateProductRequestItem


async def update_bulk_products_example():
    updated_products = await client.core.update_bulk_products(
        vendor_id=456,
        request=BatchUpdateProductsRequest(
            data=[
                UpdateProductRequestItem(
                    id=1,
                    name="Updated Product 01",
                    stock=25
                ),
                UpdateProductRequestItem(
                    id=1,
                    stock=5,
                    primary_price=21000
                )
            ]
        )
    )

    return updated_products
```

### Update Product

```python
from basalam_sdk.core.models import ProductRequestSchema

import io


async def update_product_example():
    updated_product = await client.update_product(
        product_id=789,
        request=ProductRequestSchema(
            status=3790,
            product_attribute=[
                {
                    "attribute_id": 219,
                    "value": "Suitable for formal ceremonies",
                },
                {
                    "attribute_id": 221,
                    "value": "Silk",
                },
                {
                    "attribute_id": 222,
                    "value": "Burgundy, Black, Turquoise",
                },
                {
                    "attribute_id": 1319,
                    "value": "Due to its sensitivity, this fabric should be hand washed gently with cold water.",
                }
            ]
        )
    )

    return updated_product
```

> Use
>
this [API](https://developers.basalam.com/rest/core#/operations/read_category_attribute_v3_categories__category_id__attributes_get)
> to get a list of product attributes.

### Get Product

```python
async def get_product_example():
    product = await client.get_product(
        product_id=24835037,
        prefer="return=minimal"
    )

    return product
```

### Get Products

```python
from basalam_sdk.core.models import GetProductsQuerySchema


async def get_products_example():
    products = await client.get_products(
        query_params=GetProductsQuerySchema(
            page=1,
            per_page=20,
            sort="price:asc"
        )
    )

    return products
```

### Create Products Bulk Action Request

```python
from basalam_sdk.core.models import (
    BulkProductsUpdateRequestSchema,
    ProductFilterSchema,
    BulkActionItem,
    RangeFilterItem,
    ProductBulkActionTypeEnum,
    ProductBulkFieldInputEnum
)


async def create_products_bulk_action_request_example():
    bulk_request = await client.core.create_products_bulk_action_request(
        vendor_id=456,
        request=BulkProductsUpdateRequestSchema(
            product_filter=ProductFilterSchema(
                stock=RangeFilterItem(
                    start=1,
                    end=5
                )
            ),
            action=[
                BulkActionItem(
                    field=ProductBulkFieldInputEnum.STOCK,
                    action=ProductBulkActionTypeEnum.SET,
                    value=50
                )
            ]
        )
    )

    return bulk_request
```

### Update Product Variation

```python
from basalam_sdk.core.models import UpdateProductVariationSchema


async def update_product_variation_example():
    updated_variation = await client.update_product_variation(
        product_id=789,
        variation_id=6639697,
        request=UpdateProductVariationSchema(
            primary_price=150000,
            stock=100
        )
    )

    return updated_variation
```

### Get Products Bulk Action Requests

```python
async def get_products_bulk_action_requests_example():
    bulk_requests = await client.get_products_bulk_action_requests(
        vendor_id=456,
        page=1,
        per_page=30
    )

    return bulk_requests
```

### Get Products Bulk Action Requests Count

```python
async def get_products_bulk_action_requests_count_example():
    counts = await client.get_products_bulk_action_requests_count(
        vendor_id=456
    )

    return counts
```

### Get Products Unsuccessful Bulk Action Requests

```python
async def get_products_unsuccessful_bulk_action_requests_example():
    unsuccessful_products = await client.get_products_unsuccessful_bulk_action_requests(
        request_id=123
    )

    return unsuccessful_products
```

### Get Product Shelves

```python
async def get_product_shelves_example():
    shelves = await client.get_product_shelves(
        product_id=789
    )

    return shelves
```

### Create Discount

```python
from basalam_sdk.core.models import CreateDiscountRequestSchema, DiscountProductFilterSchema


async def create_discount_example():
    discount = await client.create_discount(
        vendor_id=456,
        request=CreateDiscountRequestSchema(
            product_filter=DiscountProductFilterSchema(
                product_ids=[25010883, 24835037],
            ),
            discount_percent=20,
            active_days=5
        )
    )

    return discount
```

### Delete Discount

```python
from basalam_sdk.core.models import DeleteDiscountRequestSchema, DiscountProductFilterSchema


async def delete_discount_example():
    result = await client.create_discount(
        vendor_id=456,
        request=DeleteDiscountRequestSchema(
            product_filter=DiscountProductFilterSchema(
                product_ids=[25010883],
            )
        )
    )

    return result
```

### Get Current User

```python
async def get_current_user_example():
    user = await client.get_current_user()

    return user
```

### Create User Mobile Confirmation Request

```python
async def create_user_mobile_confirmation_request_example():
    result = await client.create_user_mobile_confirmation_request(
        user_id=123
    )

    return result
```

### Verify User Mobile Confirmation Request

```python
from basalam_sdk.core.models import ConfirmCurrentUserMobileConfirmSchema


async def verify_user_mobile_confirmation_request_example():
    result = await client.verify_user_mobile_confirmation_request(
        user_id=123,
        request=ConfirmCurrentUserMobileConfirmSchema(
            verification_code=123456
        )
    )

    return result
```

### Create User Mobile Change Request

```python
from basalam_sdk.core.models import ChangeUserMobileRequestSchema


async def create_user_mobile_change_request_example():
    result = await client.create_user_mobile_change_request(
        user_id=123,
        request=ChangeUserMobileRequestSchema(
            mobile="09123456789"
        )
    )

    return result
```

### Verify User Mobile Change Request

```python
from basalam_sdk.core.models import ChangeUserMobileConfirmSchema


async def verify_user_mobile_change_request_example():
    result = await client.verify_user_mobile_change_request(
        user_id=123,
        request=ChangeUserMobileConfirmSchema(
            mobile="09123456789",
            verification_code=123456
        )
    )

    return result
```

### Get User Bank Accounts

```python
async def get_user_bank_accounts_example():
    bank_accounts = await client.get_user_bank_accounts(
        user_id=123
    )

    return bank_accounts
```

### Create User Bank Account

```python
from basalam_sdk.core.models import UserCardsSchema


async def create_user_bank_account_example():
    bank_account = await client.create_user_bank_account(
        user_id=123,
        request=UserCardsSchema(
            card_number="1234567890123456"
        )
    )

    return bank_account
```

### Verify User Bank Account OTP

```python
from basalam_sdk.core.models import UserCardsOtpSchema


async def verify_user_bank_account_otp_example():
    result = await client.verify_user_bank_account_otp(
        user_id=123,
        request=UserCardsOtpSchema(
            card_number="1234567890123456",
            otp_code="123456"
        )
    )

    return result
```

### Verify User Bank Account

The `bank_information_id` is in the result of `verify_user_bank_account_otp` that should pass to the
`verify_user_bank_account` for verifying the new bank information just added.

```python
from basalam_sdk.core.models import UserVerifyBankInformationSchema


async def verify_user_bank_account_example():
    result = await client.verify_user_bank_account(
        user_id=123,
        request=UserVerifyBankInformationSchema(
            bank_information_id=1,
            national_code="1234567890",
            birthday="1990-01-01"
        )
    )

    return result
```

### Delete User Bank Account

```python
async def delete_user_bank_account_example():
    result = await client.delete_user_bank_account(
        user_id=123,
        bank_account_id=1
    )

    return result
```

### Update User Bank Account

```python
from basalam_sdk.core.models import UpdateUserBankInformationSchema


async def update_user_bank_account_example():
    result = await client.update_user_bank_account(
        bank_account_id=1,
        request=UpdateUserBankInformationSchema(
            user_id=123
        )
    )

    return result
```

### Update User Verification

```python
from basalam_sdk.core.models import UserVerificationSchema


async def update_user_verification_example():
    user = await client.update_user_verification(
        user_id=123,
        request=UserVerificationSchema(
            national_code="1234567890",
            birthday="1990-01-01"
        )
    )

    return user
```

### Get Category Attributes

```python
async def get_category_attributes_example():
    attributes = await client.get_category_attributes(
        category_id=1066
    )

    return attributes
```

### Get Categories

```python
async def get_categories_example():
    categories = await client.get_categories()

    return categories
```

### Get Category

```python
async def get_category_example():
    category = await client.get_category(
        category_id=1066
    )

    return category
```

### Create Shelve

```python
from basalam_sdk.core.models import ShelveSchema


async def create_shelve_example():
    shelve = await client.core.create_shelve(
        request=ShelveSchema(
            title="Summer Collection",
            description="Products for summer season"
        )
    )

    return shelve
```

### Update Shelve

```python
from basalam_sdk.core.models import ShelveSchema


async def update_shelve_example():
    shelve = await client.core.update_shelve(
        shelve_id=123,
        request=ShelveSchema(
            title="Updated Summer Collection",
            description="Updated description for summer products"
        )
    )

    return shelve
```

### Delete Shelve

```python
async def delete_shelve_example():
    result = await client.core.delete_shelve(
        shelve_id=123
    )

    return result
```

### Get Shelve Products

```python
async def get_shelve_products_example():
    # Get all products in a shelve
    products = await client.core.get_shelve_products(
        shelve_id=123
    )

    return products
```

### Update Shelve Products

```python
from basalam_sdk.core.models import UpdateShelveProductsSchema


async def update_shelve_products_example():
    # Add products to shelve
    result = await client.core.update_shelve_products(
        shelve_id=123,
        request=UpdateShelveProductsSchema(
            include_products=[456, 789, 101112],  # Product IDs to add
            exclude_products=[]
        )
    )

    # Remove products from shelve
    result = await client.core.update_shelve_products(
        shelve_id=123,
        request=UpdateShelveProductsSchema(
            include_products=[],
            exclude_products=[456, 789]  # Product IDs to remove
        )
    )

    return result
```

### Delete Shelve Product

```python
async def delete_shelve_product_example():
    result = await client.core.delete_shelve_product(
        shelve_id=123,
        product_id=456
    )

    return result
```
