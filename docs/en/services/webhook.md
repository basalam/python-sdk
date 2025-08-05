# Webhook Service

With the Webhook Service, you can receive real-time notifications about events related to your Basalam account. It
allows you to create and manage webhook subscriptions, handle various event types, monitor logs and delivery statuses,
and manage client registration and unregistration.

## Table of Contents

- [Webhook Methods](#webhook-methods)
- [Examples](#examples)

## Webhook Methods

| Method                                                  | Description                         | Parameters                       |
|---------------------------------------------------------|-------------------------------------|----------------------------------|
| [`get_webhook_services()`](#get-webhook-services)       | Get webhook services                | `None`                           |
| [`create_webhook_service()`](#create-webhook-service)   | Create a new webhook service        | `request`                        |
| [`get_webhooks()`](#get-webhooks)                       | Get list of webhooks                | `service_id`, `event_ids`        |
| [`create_webhook()`](#create-webhook)                   | Create a new webhook                | `request`                        |
| [`update_webhook()`](#update-webhook)                   | Update a webhook                    | `webhook_id`, `request`          |
| [`delete_webhook()`](#delete-webhook)                   | Delete a webhook                    | `webhook_id`                     |
| [`get_webhook_events()`](#get-webhook-events)           | Get available webhook events        | `None`                           |
| [`get_webhook_customers()`](#get-webhook-customers)     | Get customers subscribed to webhook | `page`, `per_page`, `webhook_id` |
| [`get_webhook_logs()`](#get-webhook-logs)               | Get webhook logs                    | `webhook_id`                     |
| [`register_webhook()`](#register-webhook)               | Register customer to webhook        | `request`                        |
| [`unregister_webhook()`](#unregister-webhook)           | Unregister customer from webhook    | `request`                        |
| [`get_registered_webhooks()`](#get-registered-webhooks) | Get webhooks registered by customer | `page`, `per_page`, `service_id` |

## Examples

### Initial Configuration

```python
from basalam_sdk import BasalamClient, PersonalToken

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Get Webhook Services

```python
async def get_webhook_services_example():
    services = await client.get_webhook_services()
    return services
```

### Create Webhook Service

```python
from basalam_sdk.webhook.models import CreateServiceRequest

async def create_webhook_service_example():
    service = await client.create_webhook_service(
        request=CreateServiceRequest(
            title="My Webhook Service",
            description="Service for handling order notifications"
        )
    )
    return service
```

### Get Webhooks

```python
async def get_webhooks_example():
    webhooks = await client.get_webhooks(
        service_id=1,
        event_ids="1,2,3"
    )
    return webhooks
```

### Create Webhook

```python
from basalam_sdk.webhook.models import CreateWebhookRequest

async def create_webhook_example():
    webhook = await client.create_webhook(
        request=CreateWebhookRequest(
            service_id=1,
            event_ids=[1, 2],
            request_headers="Content-Type: application/json",
            request_method=RequestMethodType.POST,
            url="https://your-app.com/webhook",
            is_active=True
        )
    )
    return webhook
```

### Update Webhook

```python
from basalam_sdk.webhook.models import UpdateWebhookRequest

async def update_webhook_example():
    updated_webhook = await client.update_webhook(
        webhook_id=123,
        request=UpdateWebhookRequest(
            event_ids=[1, 2, 3],
            request_headers="Content-Type: application/json",
            request_method=RequestMethodType.POST,
            url="https://your-app.com/webhook",
            is_active=False
        )
    )
    return updated_webhook
```

### Delete Webhook

```python
async def delete_webhook_example():
    result = await client.delete_webhook(webhook_id=123)
    return result
```

### Get Webhook Events

```python
async def get_webhook_events_example():
    events = await client.get_webhook_events()
    return events
```

Sample Response:

```python
EventListResource(
  data=[
    EventResource(
      id=1,
      name='CHAT_RECEIVED_MESSAGE',
      description='Message received in Basalam chat',
      sample_data={
        'id': 0,
        'chat_id': 0,
        'message': {
          'text': 'string',
          'files': [
            {'id': 0, 'url': 'string', 'width': 0, 'height': 0}
          ],
          'links': {},
          'entity_id': 0
        },
        'seen_at': None,
        'sender_id': 0,
        'created_at': 'string',
        'updated_at': 'string',
        'message_type': MessageTypeEnum.TEXT,
        'message_source': None
      },
      scopes='customer.chat.read'
    )
  ],
  result_count=9,
  total_count=None,
  total_page=None,
  page=1,
  per_page=10
)
```

Refer to [this document](https://developers.basalam.com/services/webhook) to review required scopes for each event.

### Get Webhook Customers

```python
async def get_webhook_customers_example():
    customers = await client.get_webhook_customers(
        page=1,
        per_page=10,
        webhook_id=123
    )
    return customers
```

### Get Webhook Logs

```python
async def get_webhook_logs_example():
    logs = await client.get_webhook_logs(webhook_id=123)
    return logs
```

### Register Customer to Webhook

```python
from basalam_sdk.webhook.models import RegisterClientRequest

async def register_webhook_example():
    result = await client.register_webhook(
        request=RegisterClientRequest(
            webhook_id=123
        )
    )
    return result
```

### Unregister Customer from Webhook

```python
from basalam_sdk.webhook.models import UnRegisterClientRequest

async def unregister_webhook_example():
    result = await client.unregister_webhook(
        request=UnRegisterClientRequest(
            webhook_id=123,
            customer_id=456
        )
    )
    return result
```

### Get Registered Webhooks

```python
async def get_registered_webhooks_example():
    webhooks = await client.get_registered_webhooks(
        page=1,
        per_page=10,
        service_id=1
    )
    return webhooks
```
