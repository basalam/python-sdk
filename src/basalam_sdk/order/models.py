"""
Data models for the Basalam Order Service.

This module contains all the data models used by the order service client.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel


class OrderStatusEnum(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatusEnum(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethodEnum(str, Enum):
    """Payment method enumeration."""
    ONLINE = "online"
    CASH_ON_DELIVERY = "cash_on_delivery"
    WALLET = "wallet"


class Address(BaseModel):
    """Address information."""
    id: int
    user_id: int
    title: str
    receiver_name: str
    receiver_phone: str
    province: str
    city: str
    address: str
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class OrderItem(BaseModel):
    """Order item information."""
    id: int
    order_id: int
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    unit_price: int
    total_price: int
    discount_amount: int = 0
    final_price: int = 0
    product_name: str = ""
    product_image: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Order(BaseModel):
    """Order information."""
    id: int
    user_id: int
    status: OrderStatusEnum
    payment_status: PaymentStatusEnum
    payment_method: PaymentMethodEnum
    total_amount: int
    shipping_amount: int
    discount_amount: int = 0
    final_amount: int = 0
    address: Address
    items: List[OrderItem] = []
    tracking_code: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class OrderCreateRequest(BaseModel):
    """Request model for creating an order."""
    address_id: int
    payment_method: PaymentMethodEnum
    items: List[Dict[str, Any]]
    coupon_code: Optional[str] = None
    description: Optional[str] = None


class OrderUpdateRequest(BaseModel):
    """Request model for updating an order."""
    status: Optional[OrderStatusEnum] = None
    payment_status: Optional[PaymentStatusEnum] = None
    tracking_code: Optional[str] = None
    description: Optional[str] = None


class OrderListResponse(BaseModel):
    """Response model for listing orders."""
    items: List[Order]
    total: int
    page: int
    per_page: int
    total_pages: int


class OrderDetailResponse(BaseModel):
    """Response model for order details."""
    order: Order
    related_orders: List[Order] = []


class OrderCancelRequest(BaseModel):
    """Request model for cancelling an order."""
    reason: str
    description: Optional[str] = None


class OrderRefundRequest(BaseModel):
    """Request model for refunding an order."""
    reason: str
    description: Optional[str] = None
    refund_amount: Optional[int] = None


class OrderPaymentRequest(BaseModel):
    """Request model for processing order payment."""
    payment_method: PaymentMethodEnum
    payment_id: Optional[str] = None
    description: Optional[str] = None


class OrderPaymentResponse(BaseModel):
    """Response model for order payment."""
    order_id: int
    payment_id: str
    payment_url: Optional[str] = None
    payment_status: PaymentStatusEnum
    created_at: datetime = datetime.now()


class OrderTrackingResponse(BaseModel):
    """Response model for order tracking."""
    order_id: int
    tracking_code: str
    status: OrderStatusEnum
    events: List[Dict[str, Any]] = []
    estimated_delivery: Optional[datetime] = None
    last_updated: datetime = datetime.now()


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class Order(str, Enum):
    """Order enum."""
    ASC = "ASC"
    DESC = "DESC"


class UnpaidInvoiceStatusEnum(str, Enum):
    """Unpaid invoice status enum."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class CreatePaymentRequestModel(BaseModel):
    """Create payment request model."""
    payment_method: str
    payment_id: Optional[str] = None
    description: Optional[str] = None


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
