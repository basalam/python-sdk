"""
Models for the Webhook service API.
"""
from datetime import datetime
from typing import List, Optional, Union, Dict, Any

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Validation error model."""
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""
    detail: List[ValidationError]


class ServiceResource(BaseModel):
    """Service resource model."""
    id: int
    name: str
    description: Optional[str] = None
    created_at: str
    updated_at: str


class ServiceListResource(BaseModel):
    """Service list resource model."""
    data: List[ServiceResource]


class CreateServiceRequest(BaseModel):
    """Create service request model."""
    name: str
    description: Optional[str] = None


class WebhookResource(BaseModel):
    """Webhook resource model."""
    id: int
    service_id: int
    url: str
    event_ids: List[str]
    is_active: bool
    created_at: str
    updated_at: str


class WebhookListResource(BaseModel):
    """Webhook list resource model."""
    data: List[WebhookResource]


class CreateWebhookRequest(BaseModel):
    """Create webhook request model."""
    service_id: int
    url: str
    event_ids: List[str]
    is_active: bool = True


class EventResource(BaseModel):
    """Event resource model."""
    id: str
    name: str
    description: Optional[str] = None
    service_id: int


class EventListResource(BaseModel):
    """Event list resource model."""
    data: List[EventResource]


class UpdateWebhookRequest(BaseModel):
    """Request model for updating a webhook."""
    event_ids: Optional[List[int]] = None
    request_headers: Optional[str] = None
    request_method: Optional[str] = None
    url: Optional[str] = None
    is_active: Optional[bool] = None


class DeleteWebhookResponse(BaseModel):
    """Response model for webhook deletion."""
    id: int
    deleted_at: Optional[datetime] = None


class WebhookLogResource(BaseModel):
    """Response model for webhook log resources."""
    id: int
    user_id: int
    status_code: int
    request: Optional[Dict[str, Any]] = None
    response: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class WebhookLogListResource(BaseModel):
    """Response model for list of webhook logs."""
    data: Optional[List[WebhookLogResource]] = None
    result_count: Optional[int] = 1
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 10


class RegisterClientRequest(BaseModel):
    """Request model for registering a client to a webhook."""
    webhook_id: int


class UnRegisterClientRequest(BaseModel):
    """Request model for unregistering a client from a webhook."""
    webhook_id: int
    customer_id: Optional[int] = None


class UnRegisterClientResponse(BaseModel):
    """Response model for client unregistration."""
    webhook_id: int
    customer_id: int
    deleted_at: Optional[datetime] = None


class ClientResource(BaseModel):
    """Response model for client resources."""
    id: int
    customer_id: int
    webhook_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ClientListResource(BaseModel):
    """Response model for list of clients."""
    data: Optional[List[ClientResource]] = None
    result_count: Optional[int] = 1
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 10


class WebhookRegisteredOnResource(BaseModel):
    """Response model for webhook registration resources."""
    id: int
    service_id: int
    customer_id: int
    events: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = True
    registered_at: Optional[datetime] = None


class WebhookRegisteredOnListResource(BaseModel):
    """Response model for list of webhook registrations."""
    data: Optional[List[WebhookRegisteredOnResource]] = None
    result_count: Optional[int] = 1
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 10
