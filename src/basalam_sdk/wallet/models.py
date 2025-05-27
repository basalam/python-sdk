"""
Models for the Basalam Wallet Service.

This module contains data models for the Wallet Service API.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class BalanceFilter(BaseModel):
    """Filter for balance requests."""
    cash: Optional[bool] = None
    settleable: Optional[bool] = None
    vendor: bool = True
    customer: bool = True


class ReasonResponse(BaseModel):
    """Reason response model."""
    id: int
    description: str


class ReferenceResponse(BaseModel):
    """Reference response model."""
    reference_type_id: int
    title: Optional[str] = None
    slug: Optional[str] = None
    reference_id: int


class CreditTypeResponse(BaseModel):
    """Credit type response model."""
    id: int
    title: str
    parent: Optional['CreditTypeResponse'] = None


class SpendCreditRequest(BaseModel):
    """Spend credit request model."""
    reason_id: int
    reference_id: int
    amount: int
    description: str
    types: Optional[List[int]] = None
    settleable: Optional[bool] = None
    references: Optional[Dict[str, int]] = None


class CreditResponse(BaseModel):
    """Credit response model."""
    id: int
    created_at: datetime
    updated_at: datetime
    expire_at: Optional[datetime] = None
    user_id: int
    client_id: Optional[int] = None
    reference_id: Optional[int] = None
    reason: Optional[ReasonResponse] = None
    amount: int
    remained_amount: int
    description: Optional[str] = None
    type: CreditTypeResponse
    references: Optional[List[ReferenceResponse]] = None


class SpendItemResponse(BaseModel):
    """Spend item response model."""
    id: int
    amount: int
    references: List[ReferenceResponse]
    credit: CreditResponse


class SpendResponse(BaseModel):
    """Spend response model."""
    created_at: datetime
    updated_at: datetime
    amount: int
    user_id: int
    reference_id: int
    reason: ReasonResponse
    rollback_reason: Optional[ReasonResponse] = None
    items: List[SpendItemResponse]
    references: List[ReferenceResponse]
    id: Optional[int] = None
    deleted_at: Optional[datetime] = None
    description: Optional[str] = None
    client_id: Optional[int] = None


class CreditCreationResponse(BaseModel):
    """Credit creation response model."""
    id: int
    client_id: int
    reference_id: int
    user_id: int
    reason: Optional[ReasonResponse] = None
    amount: int
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    credits: List[CreditResponse]
    references: Optional[List[ReferenceResponse]] = None


class HistoryItemResponse(BaseModel):
    """History item response model."""
    time: datetime
    amount: int
    subtotal: int
    description: Optional[str] = None
    main_reference_id: int
    references: List[ReferenceResponse]
    reason: Optional[ReasonResponse] = None
    related_credit: Optional[Any] = None  # NewHistoryCreditResponse
    related_spend: Optional[Any] = None  # HistorySpendResponse


class HistoryPaginationResponse(BaseModel):
    """History pagination response model."""
    data: List[HistoryItemResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_: int
    to: int


class RefundRequest(BaseModel):
    """Refund request model."""
    original_reason: int
    original_reference_id: int
    reason: int
    reference_id: int
    amount: int
    description: Optional[str] = None
    references: Optional[List[Dict[str, int]]] = None


class RollbackRefundRequest(BaseModel):
    """Rollback refund request model."""
    refund_reason: int
    rollback_refund_reason: int
    refund_reference_id: int
    reference_id: int
    description: Optional[str] = None
    references: Optional[List[Dict[str, int]]] = None


class BooleanResponse(BaseModel):
    """Boolean response model."""
    status: bool
