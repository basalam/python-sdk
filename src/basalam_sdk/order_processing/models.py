"""
Models for the Basalam Order Processing Service.

This module contains data models for the Order Processing Service API.
"""

from enum import Enum, IntEnum
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel


class ResourceStats(str, Enum):
    """Enum for resource statistics types."""
    NUMBER_OF_COUPON_USED_IN_ORDERS = "number-of-coupon-used-in-orders"
    NUMBER_OF_ORDERS_PER_CUSTOMER = "number-of-orders-per-customer"
    NUMBER_OF_PURCHASES_PER_CUSTOMER = "number-of-purchases-per-customer"
    NUMBER_OF_SALES_PER_VENDOR = "number-of-sales-per-vendor"
    NUMBER_OF_ORDERS_PER_VENDOR = "number-of-orders-per-vendor"
    NUMBER_OF_NOT_SHIPPED_ORDERS_PER_VENDOR = "number-of-not-shipped-orders-per-vendor"
    NUMBER_OF_SHIPPED_ORDERS_PER_VENDOR = "number-of-shipped-orders-per-vendor"
    NUMBER_OF_PENDING_ORDERS_PER_VENDOR = "number-of-pending-orders-per-vendor"
    NUMBER_OF_COMPLETED_ORDERS_PER_VENDOR = "number-of-completed-orders-per-vendor"
    NUMBER_OF_SALES_PER_PRODUCT = "number-of-sales-per-product"


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


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


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    current_page: int
    from_value: int
    last_page: int
    path: str
    per_page: int
    to: int
    total: int


class ValidationResponse(BaseModel):
    """Validation response model."""
    detail: List[Dict[str, Any]]


class AuthenticationResponse(BaseModel):
    """Authentication response model."""
    detail: str


class AuthorizationResponse(BaseModel):
    """Authorization response model."""
    detail: str


class FileResponse(BaseModel):
    """File response model."""
    id: int
    original: str
    format: str
    resized: Dict[str, str]


class CategoryResponse(BaseModel):
    """Category response model."""
    id: int
    title: str
    parent_id: Optional[int] = None


class ProductSummaryResponse(BaseModel):
    """Product summary response model."""
    id: int
    title: str
    url: str
    image: Optional[FileResponse] = None
    category: Optional[CategoryResponse] = None


class ProductVariationResponse(BaseModel):
    """Product variation response model."""
    id: Optional[int] = None
    title: Optional[str] = None
    color: Optional[str] = None
    color_code: Optional[str] = None
    size: Optional[str] = None


class ItemStatusResponse(BaseModel):
    """Item status response model."""
    id: int
    status: int
    status_text: str
    code: str
    created_at: str
    action_deadline: Optional[str] = None
    is_pending: Optional[bool] = None
    is_deletable: Optional[bool] = None
    description: Optional[str] = None
    more_data: Optional[Dict[str, Any]] = None


class Item(BaseModel):
    """Item model for order responses."""
    id: int
    title: str
    quantity: int
    weight: int
    price: int
    last_item_status: Optional[ItemStatusResponse] = None
    max_refund_amount: int
    product: ProductSummaryResponse
    variation: Optional[ProductVariationResponse] = None


class ItemSummary(BaseModel):
    """Item summary model for order responses."""
    id: int
    title: str
    quantity: int
    weight: int
    price: int
    product: ProductSummaryResponse
    variation: Optional[ProductVariationResponse] = None


class VendorResponse(BaseModel):
    """Vendor response model."""
    id: int
    name: str
    province: Optional[str] = None
    city: Optional[str] = None
    url_alias: Optional[str] = None
    image: Optional[FileResponse] = None


class ParcelResponse(BaseModel):
    """Parcel response model."""
    id: int
    vendor: VendorResponse
    status: int
    status_text: str
    estimate_send_at: str
    items: List[Item]
    invoice: Optional[Dict[str, Any]] = None
    status_bar: Optional[Dict[str, Any]] = None
    hint_bar: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class OrderResponse(BaseModel):
    """Order response model."""
    id: int
    hash_id: str
    paid_at: str
    parcels: List[ParcelResponse]
    customer_name: str
    customer_id: int
    total_price: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    coupon: Optional[Dict[str, Any]] = None


class OrdersResponse(BaseModel):
    """Orders list response model."""
    data: List[OrderResponse]
    meta: PaginationMeta


class ItemResponse(BaseModel):
    """Item response model for customer items endpoint."""
    id: int
    order_id: int
    product_id: int
    vendor_id: int
    customer_id: int
    price: int
    quantity: int
    weight: int
    title: str
    last_status: int
    last_status_text: str
    created_at: str
    updated_at: str
    product: ProductSummaryResponse
    vendor: VendorResponse
    variation: Optional[ProductVariationResponse] = None


class ItemsResponse(BaseModel):
    """Items list response model."""
    data: List[ItemResponse]
    meta: PaginationMeta


class OrderStatsResponse(BaseModel):
    """Order statistics response model."""
    value: int


class OrderParcelFilter(BaseModel):
    """Filter for order parcel requests."""
    ids: Optional[List[int]] = None
    customer_ids: Optional[List[int]] = None
    vendor_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    order_ids: Optional[List[int]] = None
    statuses: Optional[List[ParcelStatus]] = None
    estimate_send_at_gte: Optional[str] = None
    estimate_send_at_lte: Optional[str] = None
    created_at_gte: Optional[str] = None
    created_at_lte: Optional[str] = None
    sort: str = "estimate_send_at:desc"
    per_page: int = 10
    cursor: Optional[str] = None


class OrderFilter(BaseModel):
    """Filter for customer orders requests."""
    ids: Optional[List[int]] = None
    customer_ids: Optional[List[int]] = None
    vendor_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    item_title_like: Optional[str] = None
    parcel_statuses: Optional[List[ParcelStatus]] = None
    customer_name_like: Optional[str] = None
    paid_at_gte: Optional[str] = None
    paid_at_lte: Optional[str] = None
    parcel_estimate_send_at_lte: Optional[str] = None
    parcel_estimate_send_at_gte: Optional[str] = None
    sort: str = "paid_at:desc"
    per_page: int = 10
    cursor: Optional[str] = None


class ItemFilter(BaseModel):
    """Filter for customer items requests."""
    ids: Optional[List[int]] = None
    order_ids: Optional[List[int]] = None
    customer_ids: Optional[List[int]] = None
    product_ids: Optional[List[int]] = None
    vendor_ids: Optional[List[int]] = None
    created_at_gte: Optional[str] = None
    created_at_lte: Optional[str] = None
    sort: str = "created_at:desc"
    per_page: int = 10
    cursor: Optional[str] = None
