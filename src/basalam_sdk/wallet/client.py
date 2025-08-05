"""
Wallet service client for the Basalam SDK.

This module provides a client for interacting with Basalam's wallet service.
"""

import logging
from typing import Dict, List, Optional, Union, Any

from .models import (
    BalanceFilter,
    CanRollbackRefundResponse,
    CreditCreationResponse,
    HistoryPaginationResponse,
    RefundRequest,
    RollbackRefundRequest,
    SpendCreditRequest,
    SpendSpecificCreditRequest,
    SpendResponse,
)
from ..base_client import BaseClient

logger = logging.getLogger(__name__)


class WalletService(BaseClient):
    """
    Client for the Basalam Wallet Service API.

    This client provides methods for interacting with user balances,
    spending credits, and managing refunds.
    """

    def __init__(self, **kwargs):
        """
        Initialize the wallet service client.
        """
        super().__init__(service="wallet", **kwargs)

    # -------------------------------------------------------------------------
    # Balance endpoints
    # -------------------------------------------------------------------------

    async def get_balance(
            self,
            user_id: int,
            filters: List[BalanceFilter] = None,
            x_operator_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get a user's balances.

        Args:
            user_id: The ID of the user.
            filters: Optional list of balance filters.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The user's balance information.
        """
        endpoint = f"/v2/user/{user_id}/balance"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"filters": [filter.model_dump(exclude_none=True) for filter in (filters or [BalanceFilter()])]}
        response = await self._post(endpoint, json_data=payload, headers=headers)
        return response

    def get_balance_sync(
            self,
            user_id: int,
            filters: List[BalanceFilter] = None,
            x_operator_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get a user's balances (synchronous version).

        Args:
            user_id: The ID of the user.
            filters: Optional list of balance filters.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The user's balance information.
        """
        endpoint = f"/v2/user/{user_id}/balance"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"filters": [filter.model_dump(exclude_none=True) for filter in (filters or [BalanceFilter()])]}
        response = self._post_sync(endpoint, json_data=payload, headers=headers)
        return response

    async def get_transactions(
            self,
            user_id: int,
            page: int = 1,
            per_page: int = 50,
            x_operator_id: Optional[int] = None
    ) -> HistoryPaginationResponse:
        """
        Get a user's transaction history.

        Args:
            user_id: The ID of the user.
            page: Page number for pagination.
            per_page: Number of items per page.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The user's transaction history.
        """
        endpoint = f"/v2/user/{user_id}/history"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        params = {"page": page, "per_page": per_page}
        response = await self._get(endpoint, params=params, headers=headers)
        return HistoryPaginationResponse(**response)

    def get_transactions_sync(
            self,
            user_id: int,
            page: int = 1,
            per_page: int = 50,
            x_operator_id: Optional[int] = None
    ) -> HistoryPaginationResponse:
        """
        Get a user's transaction history (synchronous version).

        Args:
            user_id: The ID of the user.
            page: Page number for pagination.
            per_page: Number of items per page.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The user's transaction history.
        """
        endpoint = f"/v2/user/{user_id}/history"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        params = {"page": page, "per_page": per_page}
        response = self._get_sync(endpoint, params=params, headers=headers)
        print('yoyoyoyoyoyooyoyoy \n', response)
        return HistoryPaginationResponse(**response)

    # -------------------------------------------------------------------------
    # Credit spending endpoints
    # -------------------------------------------------------------------------

    async def create_expense(
            self,
            user_id: int,
            request: SpendCreditRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Create an expense from a user's balance.

        Args:
            user_id: The ID of the user.
            request: The spend credit request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The spend response.
        """
        endpoint = f"/v2/user/{user_id}/spend"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)

    async def create_expense_from_credit(
            self,
            user_id: int,
            credit_id: int,
            request: SpendSpecificCreditRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Create an expense from a specific credit.

        Args:
            user_id: The ID of the user.
            credit_id: The ID of the credit to spend from.
            request: The spend credit request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The spend response.
        """
        endpoint = f"/v2/user/{user_id}/credit/{credit_id}/spend"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)

    def create_expense_from_credit_sync(
            self,
            user_id: int,
            credit_id: int,
            request: SpendSpecificCreditRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Create an expense from a specific credit (synchronous version).

        Args:
            user_id: The ID of the user.
            credit_id: The ID of the credit to spend from.
            request: The spend credit request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The spend response.
        """
        endpoint = f"/v2/user/{user_id}/credit/{credit_id}/spend"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)

    def create_expense_sync(
            self,
            user_id: int,
            request: SpendCreditRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Create an expense from a user's balance (synchronous version).

        Args:
            user_id: The ID of the user.
            request: The spend credit request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The spend response.
        """
        endpoint = f"/v2/user/{user_id}/spend"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)

    async def get_expense(
            self,
            user_id: int,
            expense_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Get details of a specific expense.

        Args:
            user_id: The ID of the user.
            expense_id: The ID of the expense.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The expense details.
        """
        endpoint = f"/v2/user/{user_id}/spend/{expense_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._get(endpoint, headers=headers)
        return SpendResponse(**response)

    def get_expense_sync(
            self,
            user_id: int,
            expense_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Get details of a specific expense (synchronous version).

        Args:
            user_id: The ID of the user.
            expense_id: The ID of the expense.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The expense details.
        """
        endpoint = f"/v2/user/{user_id}/spend/{expense_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._get_sync(endpoint, headers=headers)
        return SpendResponse(**response)

    async def delete_expense(
            self,
            user_id: int,
            expense_id: int,
            rollback_reason_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Delete an expense.

        Args:
            user_id: The ID of the user.
            expense_id: The ID of the expense to delete.
            rollback_reason_id: The reason ID for the rollback.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = f"/v2/user/{user_id}/spend/{expense_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"rollback_reason_id": rollback_reason_id}
        response = await self._delete(endpoint, json_data=payload, headers=headers)
        return SpendResponse(**response)

    def delete_expense_sync(
            self,
            user_id: int,
            expense_id: int,
            rollback_reason_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Delete an expense (synchronous version).

        Args:
            user_id: The ID of the user.
            expense_id: The ID of the expense to delete.
            rollback_reason_id: The reason ID for the rollback.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = f"/v2/user/{user_id}/spend/{expense_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"rollback_reason_id": rollback_reason_id}
        response = self._delete_sync(endpoint, json_data=payload, headers=headers)
        return SpendResponse(**response)

    async def get_expense_by_ref(
            self,
            user_id: int,
            reason_id: int,
            reference_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Get expense details by reference.

        Args:
            user_id: The ID of the user.
            reason_id: The reason ID.
            reference_id: The reference ID.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The expense details.
        """
        endpoint = f"/v2/user/{user_id}/spend/by-ref/{reason_id}/{reference_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._get(endpoint, headers=headers)
        return SpendResponse(**response)

    def get_expense_by_ref_sync(
            self,
            user_id: int,
            reason_id: int,
            reference_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Get expense details by reference (synchronous version).

        Args:
            user_id: The ID of the user.
            reason_id: The reason ID.
            reference_id: The reference ID.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The expense details.
        """
        endpoint = f"/v2/user/{user_id}/spend/by-ref/{reason_id}/{reference_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._get_sync(endpoint, headers=headers)
        return SpendResponse(**response)

    async def delete_expense_by_ref(
            self,
            user_id: int,
            reason_id: int,
            reference_id: int,
            rollback_reason_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Delete an expense by reference.

        Args:
            user_id: The ID of the user.
            reason_id: The reason ID.
            reference_id: The reference ID.
            rollback_reason_id: The reason ID for the rollback.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = f"/v2/user/{user_id}/spend/by-ref/{reason_id}/{reference_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"rollback_reason_id": rollback_reason_id}
        response = await self._delete(endpoint, json_data=payload, headers=headers)
        return SpendResponse(**response)

    def delete_expense_by_ref_sync(
            self,
            user_id: int,
            reason_id: int,
            reference_id: int,
            rollback_reason_id: int,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Delete an expense by reference (synchronous version).

        Args:
            user_id: The ID of the user.
            reason_id: The reason ID.
            reference_id: The reference ID.
            rollback_reason_id: The reason ID for the rollback.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = f"/v2/user/{user_id}/spend/by-ref/{reason_id}/{reference_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"rollback_reason_id": rollback_reason_id}
        response = self._delete_sync(endpoint, json_data=payload, headers=headers)
        return SpendResponse(**response)

    # -------------------------------------------------------------------------
    # Refund endpoints
    # -------------------------------------------------------------------------

    async def create_refund(
            self,
            request: RefundRequest,
            x_operator_id: Optional[int] = None
    ) -> Union[CreditCreationResponse, SpendResponse]:
        """
        Create a refund.

        Args:
            request: The refund request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            Either a credit creation response or a spend response.
        """
        endpoint = "/v2/refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)

        # The API can return either a CreditCreationResponse or a SpendResponse
        # Try to parse as CreditCreationResponse first, then fallback to SpendResponse
        try:
            return CreditCreationResponse(**response)
        except:
            return SpendResponse(**response)

    def create_refund_sync(
            self,
            request: RefundRequest,
            x_operator_id: Optional[int] = None
    ) -> Union[CreditCreationResponse, SpendResponse]:
        """
        Create a refund (synchronous version).

        Args:
            request: The refund request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            Either a credit creation response or a spend response.
        """
        endpoint = "/v2/refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)

        # The API can return either a CreditCreationResponse or a SpendResponse
        # Try to parse as CreditCreationResponse first, then fallback to SpendResponse
        try:
            return CreditCreationResponse(**response)
        except:
            return SpendResponse(**response)

    async def can_rollback_refund(
            self,
            refund_reason: int,
            refund_reference_id: int,
            x_operator_id: Optional[int] = None
    ) -> CanRollbackRefundResponse:
        """
        Check if a refund can be rolled back.

        Args:
            refund_reason: The refund reason.
            refund_reference_id: The refund reference ID.
            x_operator_id: Optional operator ID for the request.

        Returns:
            Response containing status and message.
        """
        endpoint = "/v2/can-rollback-refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {
            "refund_reason": refund_reason,
            "refund_reference_id": refund_reference_id
        }
        response = await self._post(endpoint, json_data=payload, headers=headers)
        return CanRollbackRefundResponse(**response)

    def can_rollback_refund_sync(
            self,
            refund_reason: int,
            refund_reference_id: int,
            x_operator_id: Optional[int] = None
    ) -> CanRollbackRefundResponse:
        """
        Check if a refund can be rolled back (synchronous version).

        Args:
            refund_reason: The refund reason.
            refund_reference_id: The refund reference ID.
            x_operator_id: Optional operator ID for the request.

        Returns:
            Response containing status and message.
        """
        endpoint = "/v2/can-rollback-refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {
            "refund_reason": refund_reason,
            "refund_reference_id": refund_reference_id
        }
        response = self._post_sync(endpoint, json_data=payload, headers=headers)
        return CanRollbackRefundResponse(**response)

    async def rollback_refund(
            self,
            request: RollbackRefundRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Rollback a refund.

        Args:
            request: The rollback refund request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = "/v2/rollback-refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._delete(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)

    def rollback_refund_sync(
            self,
            request: RollbackRefundRequest,
            x_operator_id: Optional[int] = None
    ) -> SpendResponse:
        """
        Rollback a refund (synchronous version).

        Args:
            request: The rollback refund request.
            x_operator_id: Optional operator ID for the request.

        Returns:
            The rollback response.
        """
        endpoint = "/v2/rollback-refund"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = self._delete_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return SpendResponse(**response)
