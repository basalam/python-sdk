"""
Models for the Basalam Wallet Service.

This module contains data models for the Wallet Service API.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class BalanceFilter(BaseModel):
    """Filter for balance requests."""
    cash: Optional[bool] = None
    settleable: Optional[bool] = None
    vendor: Optional[bool] = None
    customer: Optional[bool] = None


class ReasonResponse(BaseModel):
    """Reason response model."""
    id: int
    description: str


class ReferenceResponse(BaseModel):
    """Reference response model."""
    reference_type_id: int
    title: str
    slug: str
    reference_id: int


class ReferenceRequest(BaseModel):
    """Reference response model."""
    reference_type_id: int
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
    id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    amount: int
    description: Optional[str] = None
    user_id: int
    client_id: Optional[int] = None
    reference_id: int
    reason: ReasonResponse
    rollback_reason: ReasonResponse
    items: List[SpendItemResponse]
    references: List[ReferenceResponse]


class HistoryCreditItemResponse(BaseModel):
    """History credit item response model."""
    id: int
    amount: int
    remained_amount: int
    created_at: datetime
    expire_at: Optional[datetime] = None
    type: CreditTypeResponse


class NewHistoryCreditResponse(BaseModel):
    """New history credit response model."""
    amount: Optional[int] = None
    remained_amount: Optional[int] = None
    created_at: Optional[datetime] = None
    items: Optional[List[HistoryCreditItemResponse]] = None


class HistorySpendItemResponse(BaseModel):
    """History spend item response model."""
    id: int
    amount: int


class HistorySpendResponse(BaseModel):
    """History spend response model."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    amount: Optional[int] = None
    items: Optional[List[HistorySpendItemResponse]] = None


class HistoryItemResponse(BaseModel):
    """History item response model."""
    time: datetime
    amount: int
    subtotal: int
    description: str
    main_reference_id: int
    reason: Optional[ReasonResponse] = None
    references: List[ReferenceResponse]
    related_credit: Optional[NewHistoryCreditResponse] = None
    related_spend: Optional[HistorySpendResponse] = None


class HistoryPaginationResponse(BaseModel):
    """History pagination response model."""
    data: List[HistoryItemResponse]
    total: int
    per_page: int
    current_page: int
    last_page: int
    from_: int
    to: int
