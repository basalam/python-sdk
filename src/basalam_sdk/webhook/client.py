"""
Client for the Webhook service API.
"""
from typing import Optional

from .models import (
    ServiceResource,
    ServiceListResource,
    CreateServiceRequest,
    WebhookResource,
    WebhookListResource,
    CreateWebhookRequest,
    EventListResource,
    UpdateWebhookRequest,
    DeleteWebhookResponse,
    WebhookLogListResource,
    ClientListResource,
    RegisterClientRequest,
    UnRegisterClientRequest,
    UnRegisterClientResponse,
    WebhookRegisteredOnListResource, ClientResource
)
from ..base_client import BaseClient


class WebhookService(BaseClient):
    """Client for the Webhook service API."""

    def __init__(self, **kwargs):
        """Initialize the webhook service client."""
        super().__init__(service="webhook", **kwargs)

    async def get_webhook_services(self) -> ServiceListResource:
        """
        Get a list of webhook services.

        Returns:
            The response containing the list of services.
        """
        endpoint = "/v1/services"
        response = await self._get(endpoint)
        return ServiceListResource(**response)

    def get_webhook_services_sync(self) -> ServiceListResource:
        """
        Get a list of webhook services (synchronous version).

        Returns:
            The response containing the list of services.
        """
        endpoint = "/v1/services"
        response = self._get_sync(endpoint)
        return ServiceListResource(**response)

    async def create_webhook_service(self, request: CreateServiceRequest) -> ServiceResource:
        """
        Create a new webhook service.

        Args:
            request: The service creation request.

        Returns:
            The created service resource.
        """
        endpoint = "/v1/services"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ServiceResource(**response)

    def create_webhook_service_sync(self, request: CreateServiceRequest) -> ServiceResource:
        """
        Create a new webhook service (synchronous version).

        Args:
            request: The service creation request.

        Returns:
            The created service resource.
        """
        endpoint = "/v1/services"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ServiceResource(**response)

    async def get_webhooks(
            self,
            service_id: Optional[int] = None,
            event_ids: Optional[str] = None
    ) -> WebhookListResource:
        """
        Get a list of webhooks.

        Args:
            service_id: Optional service ID to filter by.
            event_ids: Optional comma-separated list of event IDs to filter by.

        Returns:
            The response containing the list of webhooks.
        """
        endpoint = "/v1/webhooks"
        params = {}
        if service_id is not None:
            params["service_id"] = service_id
        if event_ids is not None:
            params["event_ids"] = event_ids

        response = await self._get(endpoint, params=params)
        return WebhookListResource(**response)

    def get_webhooks_sync(
            self,
            service_id: Optional[int] = None,
            event_ids: Optional[str] = None
    ) -> WebhookListResource:
        """
        Get a list of webhooks (synchronous version).

        Args:
            service_id: Optional service ID to filter by.
            event_ids: Optional comma-separated list of event IDs to filter by.

        Returns:
            The response containing the list of webhooks.
        """
        endpoint = "/v1/webhooks"
        params = {}
        if service_id is not None:
            params["service_id"] = service_id
        if event_ids is not None:
            params["event_ids"] = event_ids

        response = self._get_sync(endpoint, params=params)
        return WebhookListResource(**response)

    async def create_webhook(self, request: CreateWebhookRequest) -> WebhookResource:
        """
        Create a new webhook.

        Args:
            request: The webhook creation request.

        Returns:
            The created webhook resource.
        """
        endpoint = "/v1/webhooks"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return WebhookResource(**response)

    def create_webhook_sync(self, request: CreateWebhookRequest) -> WebhookResource:
        """
        Create a new webhook (synchronous version).

        Args:
            request: The webhook creation request.

        Returns:
            The created webhook resource.
        """
        endpoint = "/v1/webhooks"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return WebhookResource(**response)

    async def get_webhook_events(self) -> EventListResource:
        """
        Get a list of webhook events.

        Returns:
            The response containing the list of events.
        """
        endpoint = "/v1/webhooks/events"
        response = await self._get(endpoint)
        return EventListResource(**response)

    def get_webhook_events_sync(self) -> EventListResource:
        """
        Get a list of webhook events (synchronous version).

        Returns:
            The response containing the list of events.
        """
        endpoint = "/v1/webhooks/events"
        response = self._get_sync(endpoint)
        return EventListResource(**response)

    async def get_webhook_customers(
            self,
            page: Optional[int] = 1,
            per_page: Optional[int] = 10,
            webhook_id: Optional[int] = None
    ) -> ClientListResource:
        """
        Get a list of webhook customers.

        Args:
            page: Page number for pagination.
            per_page: Number of items per page.
            webhook_id: Optional webhook ID to filter by.

        Returns:
            The response containing the list of customers.
        """
        endpoint = "/v1/webhooks/customers"
        params = {
            "page": page,
            "per_page": per_page
        }
        if webhook_id is not None:
            params["webhook_id"] = webhook_id

        response = await self._get(endpoint, params=params)
        return ClientListResource(**response)

    def get_webhook_customers_sync(
            self,
            page: Optional[int] = 1,
            per_page: Optional[int] = 10,
            webhook_id: Optional[int] = None
    ) -> ClientListResource:
        """
        Get a list of webhook customers (synchronous version).

        Args:
            page: Page number for pagination.
            per_page: Number of items per page.
            webhook_id: Optional webhook ID to filter by.

        Returns:
            The response containing the list of customers.
        """
        endpoint = "/v1/webhooks/customers"
        params = {
            "page": page,
            "per_page": per_page
        }
        if webhook_id is not None:
            params["webhook_id"] = webhook_id

        response = self._get_sync(endpoint, params=params)
        return ClientListResource(**response)

    async def update_webhook(
            self,
            webhook_id: int,
            request: UpdateWebhookRequest
    ) -> WebhookResource:
        """
        Update a webhook.

        Args:
            webhook_id: The ID of the webhook to update.
            request: The update request.

        Returns:
            The updated webhook resource.
        """
        endpoint = f"/v1/webhooks/{webhook_id}"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True))
        return WebhookResource(**response)

    def update_webhook_sync(
            self,
            webhook_id: int,
            request: UpdateWebhookRequest
    ) -> WebhookResource:
        """
        Update a webhook (synchronous version).

        Args:
            webhook_id: The ID of the webhook to update.
            request: The update request.

        Returns:
            The updated webhook resource.
        """
        endpoint = f"/v1/webhooks/{webhook_id}"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return WebhookResource(**response)

    async def delete_webhook(self, webhook_id: int) -> DeleteWebhookResponse:
        """
        Delete a webhook.

        Args:
            webhook_id: The ID of the webhook to delete.

        Returns:
            The deletion response.
        """
        endpoint = f"/v1/webhooks/{webhook_id}"
        response = await self._delete(endpoint)
        return DeleteWebhookResponse(**response)

    def delete_webhook_sync(self, webhook_id: int) -> DeleteWebhookResponse:
        """
        Delete a webhook (synchronous version).

        Args:
            webhook_id: The ID of the webhook to delete.

        Returns:
            The deletion response.
        """
        endpoint = f"/v1/webhooks/{webhook_id}"
        response = self._delete_sync(endpoint)
        return DeleteWebhookResponse(**response)

    async def get_webhook_logs(self, webhook_id: int) -> WebhookLogListResource:
        """
        Get logs for a webhook.

        Args:
            webhook_id: The ID of the webhook to get logs for.

        Returns:
            The response containing the webhook logs.
        """
        endpoint = f"/v1/webhooks/{webhook_id}/logs"
        response = await self._get(endpoint)
        return WebhookLogListResource(**response)

    def get_webhook_logs_sync(self, webhook_id: int) -> WebhookLogListResource:
        """
        Get logs for a webhook (synchronous version).

        Args:
            webhook_id: The ID of the webhook to get logs for.

        Returns:
            The response containing the webhook logs.
        """
        endpoint = f"/v1/webhooks/{webhook_id}/logs"
        response = self._get_sync(endpoint)
        return WebhookLogListResource(**response)

    async def register_webhook(self, request: RegisterClientRequest) -> ClientResource:
        """
        Register a client to a webhook.

        Args:
            request: The registration request.

        Returns:
            The created client resource.
        """
        endpoint = "/v1/customers/webhooks"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True))
        return ClientResource(**response)

    def register_webhook_sync(self, request: RegisterClientRequest) -> ClientResource:
        """
        Register a client to a webhook (synchronous version).

        Args:
            request: The registration request.

        Returns:
            The created client resource.
        """
        endpoint = "/v1/customers/webhooks"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return ClientResource(**response)

    async def unregister_webhook(self, request: UnRegisterClientRequest) -> UnRegisterClientResponse:
        """
        Unregister a customer from a webhook.

        Args:
            request: The unregistration request.

        Returns:
            The unregistration response.
        """
        endpoint = "/v1/customers/webhooks"
        response = await self._delete(endpoint, json_data=request.model_dump(exclude_none=True))
        return UnRegisterClientResponse(**response)

    def unregister_webhook_sync(self, request: UnRegisterClientRequest) -> UnRegisterClientResponse:
        """
        Unregister a customer from a webhook (synchronous version).

        Args:
            request: The unregistration request.

        Returns:
            The unregistration response.
        """
        endpoint = "/v1/customers/webhooks"
        response = self._delete_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return UnRegisterClientResponse(**response)

    async def get_registered_webhooks(
            self,
            page: Optional[int] = 1,
            per_page: Optional[int] = 10,
            service_id: Optional[int] = None
    ) -> WebhookRegisteredOnListResource:
        """
        Get webhooks that the customer is registered on.

        Args:
            page: Page number for pagination.
            per_page: Number of items per page.
            service_id: Optional service ID to filter by.

        Returns:
            The response containing the list of registered webhooks.
        """
        endpoint = "/v1/customers/webhooks"
        params = {
            "page": page,
            "per_page": per_page
        }
        if service_id is not None:
            params["service_id"] = service_id

        response = await self._get(endpoint, params=params)
        return WebhookRegisteredOnListResource(**response)

    def get_registered_webhooks_sync(
            self,
            page: Optional[int] = 1,
            per_page: Optional[int] = 10,
            service_id: Optional[int] = None
    ) -> WebhookRegisteredOnListResource:
        """
        Get webhooks that the customer is registered on (synchronous version).

        Args:
            page: Page number for pagination.
            per_page: Number of items per page.
            service_id: Optional service ID to filter by.

        Returns:
            The response containing the list of registered webhooks.
        """
        endpoint = "/v1/customers/webhooks"
        params = {
            "page": page,
            "per_page": per_page
        }
        if service_id is not None:
            params["service_id"] = service_id

        response = self._get_sync(endpoint, params=params)
        return WebhookRegisteredOnListResource(**response)
