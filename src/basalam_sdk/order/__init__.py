"""
OrderEnum service module for the Basalam SDK.

This module provides the order service client and related models for interacting
with Basalam's order service.
"""

from .client import OrderService
from .models import (
    # Enums
    OrderEnum,
    UnpaidInvoiceStatusEnum,

    # Core Models
    City,

    # Payment Models
    CreatePaymentRequestModel,
    PaymentCallbackRequestModel,
    PaymentVerifyRequestModel,
    PaymentDriver,

    # Basket Models
    BasketAddress,
    BasketCosts,
    BasketProduct,
    BasketProductCategory,
    BasketProductPhoto,
    BasketResponse,
    BasketVariation,
    BasketVariationProperty,
    BasketVendor,
    BasketVendorItem,

    # Cost Models
    CostBreakdown,
    TotalCostBreakdown,

    # Origin Models
    Origin,
    OriginParcel,
    OriginShippingMethod,
    ShippingMethodInfo,

    # Vendor Models
    VendorOwner,
    VendorOwnerAvatar,
)

__all__ = [
    # Client
    "OrderService",

    # Enums
    "OrderEnum",
    "UnpaidInvoiceStatusEnum",

    # Core Models
    "City",

    # Payment Models
    "CreatePaymentRequestModel",
    "PaymentCallbackRequestModel",
    "PaymentVerifyRequestModel",
    "PaymentDriver",

    # Basket Models
    "BasketAddress",
    "BasketCosts",
    "BasketProduct",
    "BasketProductCategory",
    "BasketProductPhoto",
    "BasketResponse",
    "BasketVariation",
    "BasketVariationProperty",
    "BasketVendor",
    "BasketVendorItem",

    # Cost Models
    "CostBreakdown",
    "TotalCostBreakdown",

    # Origin Models
    "Origin",
    "OriginParcel",
    "OriginShippingMethod",
    "ShippingMethodInfo",

    # Vendor Models
    "VendorOwner",
    "VendorOwnerAvatar",
]
