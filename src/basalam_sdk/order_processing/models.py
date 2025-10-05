"""
Models for the Basalam OrderEnum Processing Service.

This module contains data models for the OrderEnum Processing Service API.
"""

from enum import Enum, IntEnum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel


class ResourceStats(str, Enum):
    """Enum for resource statistics types."""
    NUMBER_OF_COUPON_USED_IN_ORDERS = "number-of-coupon-used-in-orders"
    NUMBER_OF_PURCHASES_PER_CUSTOMER = "number-of-purchases-per-customer"
    NUMBER_OF_ORDERS_PER_CUSTOMER = "number-of-orders-per-customer"
    TOTAL_OF_PURCHASE_AMOUNT_PER_CUSTOMER = "total-of-purchase-amount-per-customer"
    NUMBER_OF_SALES_PER_VENDOR = "number-of-sales-per-vendor"
    NUMBER_OF_ORDERS_PER_VENDOR = "number-of-orders-per-vendor"
    NUMBER_OF_NEW_ORDERS_PER_VENDOR = "number-of-new-orders-per-vendor"
    NUMBER_OF_PROBLEM_ORDERS_PER_VENDOR = "number-of-problem-orders-per-vendor"
    NUMBER_OF_DUE_ORDERS_PER_VENDOR = "number-of-due-orders-per-vendor"
    TOTAL_OF_SALES_AMOUNT_PER_VENDOR = "total-of-sales-amount-per-vendor"
    NUMBER_OF_SALES_PER_PRODUCT = "number-of-sales-per-product"
    NUMBER_OF_NOT_SHIPPED_ORDERS_PER_VENDOR = "number-of-not-shipped-orders-per-vendor"
    NUMBER_OF_SHIPPED_ORDERS_PER_VENDOR = "number-of-shipped-orders-per-vendor"
    NUMBER_OF_PENDING_ORDERS_PER_VENDOR = "number-of-pending-orders-per-vendor"
    NUMBER_OF_COMPLETED_ORDERS_PER_VENDOR = "number-of-completed-orders-per-vendor"


class HintVariantEnum(str, Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    SUCCESS = "success"
    NORMAL = "normal"


class ParcelStatus(IntEnum):
    """Enum for parcel status."""
    NEW_ORDER = 3739
    PREPARATION_IN_PROGRESS = 3237
    POSTED = 3238
    WRONG_TRACKING_CODE = 5017
    PRODUCT_IS_NOT_DELIVERED = 3572
    PROBLEM_IS_REPORTED = 3740
    CUSTOMER_CANCEL_REQUEST_FROM_CUSTOMER = 4633
    OVERDUE_AGREEMENT_REQUEST_FROM_VENDOR = 5075
    SATISFIED = 3195
    DEFINITIVE_DISSATISFACTION = 3233
    CANCEL = 3067


class FileResponse(BaseModel):
    """File response model."""
    id: int
    original: str
    format: Optional[str] = None
    resized: Dict[str, str]


class AmountDrivers(BaseModel):
    """Amount drivers model."""
    gateway: int
    credit: int
    salampay: int
    other: int
    total: int
    other_drivers_detail: Dict[str, Any]


class City(BaseModel):
    """City model."""
    id: int
    title: str
    parent: Optional['City'] = None


class User(BaseModel):
    """User model."""
    id: int
    hash_id: str
    name: str
    avatar: Optional[FileResponse] = None


class Recipient(BaseModel):
    """Recipient model."""
    name: str
    mobile: Optional[str] = None
    postal_code: Optional[str] = None
    postal_address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    house_number: Optional[str] = None
    house_unit: Optional[str] = None


class Customer(BaseModel):
    """Customer model."""
    recipient: Recipient
    city: Optional[City] = None
    user: User


class Status(BaseModel):
    """Status model."""
    id: int
    title: str


class ShippingMethodOption(BaseModel):
    """Shipping method option model."""
    id: int
    title: str


class ShippingMethod(BaseModel):
    """Shipping method model."""
    current: ShippingMethodOption
    default: ShippingMethodOption


class Vendor(BaseModel):
    """Vendor model."""
    id: int
    identifier: str
    title: str
    city: City
    owner: User
    logo: Optional[FileResponse] = None


class Product(BaseModel):
    """Product model."""
    id: int
    name: Optional[str] = None
    category_id: int
    photos: List[FileResponse]


class Property(BaseModel):
    """Property model."""
    id: int
    title: str
    type: str


class PropertyValue(BaseModel):
    """Property value model."""
    id: int
    title: str
    value: str


class VariationProperty(BaseModel):
    """Variation property model."""
    property: Property
    value: PropertyValue


class Variation(BaseModel):
    """Variation model."""
    id: int
    properties: Optional[List[VariationProperty]] = None


class ParcelItem(BaseModel):
    """Parcel item model."""
    id: int
    title: str
    quantity: int
    weight: float
    net_weight: Optional[float] = None
    price: int
    product: Product
    variation: Optional[Variation] = None


class Parcel(BaseModel):
    """Parcel model."""
    id: int
    total_items_price: int
    created_at: str
    updated_at: str
    estimate_send_at: Optional[str] = None
    status: Optional[Status] = None
    shipping_method: ShippingMethod
    vendor: Vendor
    items: List[ParcelItem]


class Order(BaseModel):
    """Order model."""
    id: int
    amount_drivers: AmountDrivers
    amount: int
    has_credit: bool
    bnpl_amount: int
    installment_amount: int
    coupon_discount: int
    credit_amount: int
    paid_at: str
    coupon_code: Optional[str] = None
    created_at: str
    customer: Customer
    parcels: List[Parcel]


class ParcelListItem(BaseModel):
    """Item model for parcels list response."""
    id: int
    title: str
    quantity: int
    weight: int
    net_weight: Optional[int] = None
    price: int
    product: Product
    variation: Optional[Variation] = None


class ItemStatus(BaseModel):
    """Item status model."""
    id: int
    title: str


class ItemStatusOperator(BaseModel):
    """Item status operator model."""
    id: int
    title: str


class ItemLastStatus(BaseModel):
    """Item last status model."""
    id: int
    status: ItemStatus
    operator: ItemStatusOperator
    description: Optional[str] = None
    created_at: Optional[str] = None
    details: Dict[str, Any]


class ParcelItemResponse(BaseModel):
    """Parcel item response model."""
    id: int
    title: str
    quantity: int
    weight: int
    price: int
    last_item_status: Optional[ItemLastStatus] = None
    max_refund_amount: int
    product: Product
    variation: Optional[Variation] = None


class ParcelOrder(BaseModel):
    """Parcel order model."""
    id: int
    paid_at: str
    created_at: str
    customer: Customer


class PostReceiptAttachment(BaseModel):
    """Post receipt attachment model."""
    id: int
    original: str
    format: Optional[str] = None
    resized: Dict[str, str]


class PostReceipt(BaseModel):
    """Post receipt model."""
    id: int
    tracking_code: Optional[str] = None
    final_post_cost: Optional[int] = None
    created_at: str
    updated_at: str
    tracking_link: Optional[str] = None
    phone_number: Optional[str] = None
    attachment: Optional[PostReceiptAttachment] = None
    editable: bool
    edited: bool


class ParcelResponse(BaseModel):
    """Parcel response model."""
    id: int
    total_items_price: int
    estimate_send_at: Optional[str] = None
    created_at: str
    updated_at: str
    confirmed_at: str
    send_at: Optional[str] = None
    delivery_at: str
    is_confirmed: bool
    is_send_date: bool
    is_delivered: bool
    has_delay: Optional[bool] = None
    delay_days: int
    shipping_cost: int
    shipping_method: ShippingMethod
    status: Optional[Status] = None
    vendor: Vendor
    items: List[ParcelItemResponse]
    order: ParcelOrder
    post_receipt: Optional[PostReceipt] = None


class OrdersResponse(BaseModel):
    """Orders list response model."""
    data: List[Order]
    next_cursor: Optional[str] = None
    previous_cursor: Optional[str] = None


class OrderStatsResponse(BaseModel):
    """OrderEnum statistics response model."""
    result: int


class ParcelSummaryResponse(BaseModel):
    """Summary response model for parcels."""
    id: int
    total_items_price: int
    created_at: str
    updated_at: str
    weight: int
    estimate_send_at: Optional[str] = None
    vendor: Vendor
    order: ParcelOrder
    status: Optional[Status] = None
    shipping_method: ShippingMethod
    items: List[ParcelListItem]
    post_receipt: Optional[PostReceipt] = None


class ParcelsResponse(BaseModel):
    """Parcels list response model."""
    data: List[ParcelSummaryResponse]
    next_cursor: Optional[str] = None
    previous_cursor: Optional[str] = None


class OrderParcelFilter(BaseModel):
    """Filter for order parcel requests."""
    created_at: Optional[str] = None
    cursor: Optional[str] = None
    estimate_send_at: Optional[str] = None
    ids: Optional[str] = None
    items_customer_ids: Optional[str] = None
    items_order_ids: Optional[str] = None
    items_product_ids: Optional[List[str]] = None
    items_vendor_ids: Optional[List[str]] = None
    per_page: Optional[int] = 10
    sort: Optional[str] = "estimate_send_at:desc"
    statuses: Optional[List[ParcelStatus]] = None


class OrderFilter(BaseModel):
    """Filter for customer orders requests."""
    coupon_code: Optional[str] = None
    cursor: Optional[str] = None
    customer_ids: Optional[List[str]] = None
    customer_name: Optional[str] = None
    ids: Optional[str] = None
    items_title: Optional[str] = None
    paid_at: Optional[str] = None
    parcel_estimate_send_at: Optional[str] = None
    parcel_statuses: Optional[List[str]] = None
    per_page: Optional[int] = 10
    product_ids: Optional[str] = None
    sort: Optional[str] = "paid_at:desc"
    vendor_ids: Optional[str] = None


class CustomerItemParcel(BaseModel):
    """Parcel information for customer item response."""
    id: int
    created_at: str
    updated_at: str
    estimate_send_at: str
    status: Status
    shipping_method: ShippingMethod
    vendor: Vendor


class CustomerItemResponse(BaseModel):
    """Customer item response model."""
    id: int
    title: str
    quantity: int
    weight: int
    price: int
    last_item_status: Optional[ItemLastStatus] = None
    parcel: CustomerItemParcel
    order: ParcelOrder
    product: Product
    variation: Optional[Variation] = None


class CustomerItemsResponse(BaseModel):
    """Customer items list response model."""
    data: List[CustomerItemResponse]
    next_cursor: Optional[str] = None
    previous_cursor: Optional[str] = None


class ItemFilter(BaseModel):
    """Filter for customer items requests."""
    created_at: Optional[str] = None
    cursor: Optional[str] = None
    customer_ids: Optional[str] = None
    ids: Optional[str] = None
    order_ids: Optional[str] = None
    per_page: Optional[int] = 10
    product_ids: Optional[str] = None
    sort: Optional[str] = "created_at:desc"
    vendor_ids: Optional[List[str]] = None


class Action(BaseModel):
    icon: Optional[str] = None
    variant: Optional[str] = None
    key: str
    title: str


class Hint(BaseModel):
    title: str
    text: Optional[str] = None
    actions: Optional[List[Action]] = None


class CustomerHint(BaseModel):
    variant: HintVariantEnum
    hint: Hint


class ParcelHint(BaseModel):
    id: int
    hint_bar: Optional[CustomerHint] = None


class ParcelHintsResponse(BaseModel):
    """Response model for parcel hints of a customer order."""
    id: int
    parcels: List[ParcelHint]
