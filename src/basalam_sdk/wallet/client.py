"""
Wallet service client for the Basalam SDK.

This module provides a client for interacting with Basalam's wallet service.
"""

import logging
from typing import Dict, List, Optional, Union, Any

from .models import (
    BalanceFilter,
    HistoryPaginationResponse,
    SpendCreditRequest,
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
        endpoint = f"/v1/users/{user_id}/balance"
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
        endpoint = f"/v1/users/{user_id}/balance"
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
        endpoint = f"/v1/users/{user_id}/transactions"
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
        endpoint = f"/v1/users/{user_id}/transactions"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        params = {"page": page, "per_page": per_page}
        response = self._get_sync(endpoint, params=params, headers=headers)
        return HistoryPaginationResponse(**response)

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
        endpoint = f"/v1/users/{user_id}/expenses"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
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
        endpoint = f"/v1/users/{user_id}/expenses"
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
        endpoint = f"/v1/users/{user_id}/expenses/{expense_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/{expense_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/{expense_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/{expense_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/by-ref/{reason_id}/{reference_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/by-ref/{reason_id}/{reference_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/by-ref/{reason_id}/{reference_id}"
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
        endpoint = f"/v1/users/{user_id}/expenses/by-ref/{reason_id}/{reference_id}"
        headers = {}
        if x_operator_id is not None:
            headers["x-operator-id"] = str(x_operator_id)

        payload = {"rollback_reason_id": rollback_reason_id}
        response = self._delete_sync(endpoint, json_data=payload, headers=headers)
        return SpendResponse(**response)
