"""
Wallet service client for the Basalam SDK.

This module provides access to Basalam's wallet service APIs.
"""

from .client import WalletService
from .models import (
    BalanceFilter,
    BalanceResponse,
    HistoryPaginationResponse,
    ReferenceRequestModel,
    ReferenceTypeEnum,
    SpendCreditRequest,
    SpendResponse,
    RefundRequest,
    ClientTransferResponse,
    ClientCreditResponse,
    CreditResponse,
    CreditMainTypeEnum,
    CreditCreationRequest,
    CreditCreationResponse,
    RollbackRefundRequest,
    ReasonResponse,
    DeleteTransferResponse
)

__all__ = [
    "WalletService",
    "BalanceFilter",
    "BalanceResponse",
    "HistoryPaginationResponse",
    "ReferenceRequestModel",
    "ReferenceTypeEnum",
    "SpendCreditRequest",
    "SpendResponse",
    "RefundRequest",
    "ClientTransferResponse",
    "ClientCreditResponse",
    "CreditResponse",
    "CreditMainTypeEnum",
    "CreditCreationRequest",
    "CreditCreationResponse",
    "RollbackRefundRequest",
    "ReasonResponse",
    "DeleteTransferResponse"
]
