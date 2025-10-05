"""
Wallet service client for the Basalam SDK.

This module provides access to Basalam's wallet service APIs.
"""

from .client import WalletService
from .models import (
    BalanceFilter,
    CreditResponse,
    CreditTypeResponse,
    HistoryCreditItemResponse,
    HistoryItemResponse,
    HistoryPaginationResponse,
    HistorySpendItemResponse,
    HistorySpendResponse,
    NewHistoryCreditResponse,
    ReasonResponse,
    ReferenceRequest,
    ReferenceResponse,
    SpendCreditRequest,
    SpendItemResponse,
    SpendResponse,
)

__all__ = [
    "WalletService",
    "BalanceFilter",
    "CreditResponse",
    "CreditTypeResponse",
    "HistoryCreditItemResponse",
    "HistoryItemResponse",
    "HistoryPaginationResponse",
    "HistorySpendItemResponse",
    "HistorySpendResponse",
    "NewHistoryCreditResponse",
    "ReasonResponse",
    "ReferenceRequest",
    "ReferenceResponse",
    "SpendCreditRequest",
    "SpendItemResponse",
    "SpendResponse",
]
