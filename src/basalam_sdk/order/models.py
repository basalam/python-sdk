"""
Data models for the Basalam OrderEnum Service.

This module contains all the data models used by the order service client.
"""

from enum import Enum
from typing import Dict, List, Optional, Any

from pydantic import BaseModel


class City(BaseModel):
    """City model."""
    id: Optional[int] = None
    title: Optional[str] = None
    parent: Optional['City'] = None


class OrderEnum(str, Enum):
    """OrderEnum enum."""
    ASC = "ASC"
    DESC = "DESC"


class UnpaidInvoiceStatusEnum(str, Enum):
    """Unpaid invoice status enum."""
    SALEABLE = "saleable"
    PAYABLE = "payable"
    UNPAID = "unpaid"


class PaymentDriver(BaseModel):
    """Payment driver model."""
    amount: int


class CreatePaymentRequestModel(BaseModel):
    """Create payment request model."""
    pay_drivers: Dict[str, PaymentDriver]
    callback: str
    option_code: Optional[str] = None
    national_id: Optional[str] = None


class PaymentCallbackRequestModel(BaseModel):
    """Payment callback request model."""
    status: str
    transaction_id: Optional[str] = None
    description: Optional[str] = None


class PaymentVerifyRequestModel(BaseModel):
    """Payment verify request model."""
    payment_id: str
    transaction_id: Optional[str] = None
    description: Optional[str] = None


# Basket Models - Updated for new structure

class CostBreakdown(BaseModel):
    """Cost breakdown model."""
    base: Optional[int] = None
    discount: Optional[int] = None
    grand: Optional[int] = None


class TotalCostBreakdown(BaseModel):
    """Total cost breakdown model."""
    base: Optional[int] = None
    discount: Optional[int] = None
    credit: Optional[int] = None
    bnpl: Optional[int] = None
    installment: Optional[int] = None
    pay_lines: Optional[int] = None
    grand: Optional[int] = None


class BasketCosts(BaseModel):
    """Basket costs model."""
    delivery: Optional[CostBreakdown] = None
    products: Optional[CostBreakdown] = None
    total: Optional[TotalCostBreakdown] = None


class BasketAddress(BaseModel):
    """Basket address model."""
    id: Optional[int] = None
    name: Optional[str] = None
    mobile: Optional[str] = None
    tel: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: Optional[bool] = None
    city: Optional[City] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    house_number: Optional[str] = None
    house_unit: Optional[str] = None


class ShippingMethodInfo(BaseModel):
    """Shipping method information."""
    id: Optional[int] = None
    title: Optional[str] = None
    parent: Optional[Dict[str, Any]] = None


class OriginShippingMethod(BaseModel):
    """Origin shipping method model."""
    id: Optional[int] = None
    method: Optional[ShippingMethodInfo] = None
    delivery_time: Optional[int] = None
    warehouse: Optional[Dict[str, Any]] = None


class OriginParcel(BaseModel):
    """Origin parcel model."""
    id: Optional[int] = None
    shipping_method: Optional[OriginShippingMethod] = None
    preparation_days: Optional[int] = None
    delivery_days: Optional[int] = None
    arrival_delivery_days: Optional[int] = None


class Origin(BaseModel):
    """Origin model."""
    id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    parcel: Optional[OriginParcel] = None
    city: Optional[City] = None
    is_warehouse: Optional[bool] = None
    vendor_identifiers: Optional[List[int]] = None
    delivery_costs: Optional[CostBreakdown] = None


class BasketProductPhoto(BaseModel):
    """Basket product photo model."""
    id: Optional[int] = None
    original: Optional[str] = None
    resized: Optional[Dict[str, str]] = None


class BasketProductCategory(BaseModel):
    """Basket product category model."""
    id: Optional[int] = None
    title: Optional[str] = None


class BasketProduct(BaseModel):
    """Basket product model."""
    id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[int] = None
    primary_price: Optional[int] = None
    stock: Optional[int] = None
    category: Optional[BasketProductCategory] = None
    photos: Optional[List[BasketProductPhoto]] = None


class BasketVariationProperty(BaseModel):
    """Basket variation property model."""
    property: Optional[Dict[str, Any]] = None
    value: Optional[Dict[str, Any]] = None


class BasketVariation(BaseModel):
    """Basket variation model."""
    id: Optional[int] = None
    stock: Optional[int] = None
    price: Optional[int] = None
    primary_price: Optional[int] = None
    properties: Optional[List[BasketVariationProperty]] = None


class BasketVendorItem(BaseModel):
    """Basket vendor item model."""
    id: Optional[int] = None
    parcel_id: Optional[int] = None
    title: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[int] = None
    primary_price: Optional[int] = None
    payable_amount: Optional[int] = None
    delivery_cost: Optional[int] = None
    total_discount: Optional[int] = None
    basalam_product_discount: Optional[int] = None
    basalam_delivery_discount: Optional[int] = None
    vendor_product_discount: Optional[int] = None
    vendor_delivery_discount: Optional[int] = None
    public_delivery_discount: Optional[int] = None
    product: Optional[BasketProduct] = None
    variation: Optional[BasketVariation] = None
    vendor_coupon: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    comment: Optional[str] = None
    is_deleted: Optional[bool] = None


class VendorOwnerAvatar(BaseModel):
    """Vendor owner avatar model."""
    id: Optional[int] = None
    original: Optional[str] = None
    resized: Optional[Dict[str, str]] = None


class VendorOwner(BaseModel):
    """Vendor owner model."""
    id: Optional[int] = None
    hash_id: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[VendorOwnerAvatar] = None
    city: Optional[City] = None


class BasketVendor(BaseModel):
    """Basket vendor model."""
    id: Optional[int] = None
    identifier: Optional[str] = None
    url_alias: Optional[str] = None
    title: Optional[str] = None
    logo: Optional[Dict[str, Any]] = None
    owner: Optional[VendorOwner] = None
    total_product_amount: Optional[int] = None
    free_shipping_amount: Optional[int] = None
    free_shipping_type: Optional[str] = None
    items: Optional[List[BasketVendorItem]] = None
    city: Optional[City] = None
    parcel_identifiers: Optional[List[int]] = None
    origin_identifiers: Optional[List[int]] = None
    preparation_days: Optional[int] = None
    delivery_days: Optional[int] = None
    arrival_days: Optional[int] = None
    delivery_costs: Optional[CostBreakdown] = None


class BasketResponse(BaseModel):
    """Response model for basket endpoint."""
    id: Optional[int] = None
    item_count: Optional[int] = None
    show_recipient_mobile: Optional[bool] = None
    delivery_method: Optional[str] = None
    costs: Optional[BasketCosts] = None
    errors: Optional[List[str]] = None
    error_count: Optional[int] = None
    coupon: Optional[Dict[str, Any]] = None
    option_code: Optional[str] = None
    address: Optional[BasketAddress] = None
    origins: Optional[List[Origin]] = None
    vendors: Optional[List[BasketVendor]] = None
