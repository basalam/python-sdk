# Chat Service

Handle messaging and chat functionalities with the Chat Service. This service provides comprehensive tools for managing
conversations, messages, and chat interactions: create and manage chat conversations, send and retrieve messages, handle
different message types, manage chat participants, and track chat history and updates.

## Table of Contents

- [Chat Methods](#chat-methods)
- [Bot Methods](#bot-methods)
- [Examples](#examples)

## Chat Methods

| Method                                              | Description                 | Parameters                          |
|-----------------------------------------------------|-----------------------------|-------------------------------------|
| [`create_message()`](#create-message)               | Create a message            | `request: MessageRequest`           |
| [`create_chat()`](#create-chat)                     | Create a chat               | `request: CreateChatRequest`        |
| [`get_messages()`](#get-messages)                   | Get chat messages           | `request: GetMessagesRequest`       |
| [`get_chats()`](#get-chats)                         | Get chats list              | `request: GetChatsRequest`          |
| [`edit_message()`](#edit-message)                   | Edit an existing message    | `request: EditMessageRequest`       |
| [`delete_message()`](#delete-message)               | Delete messages             | `request: DeleteMessageRequest`     |
| [`delete_chats()`](#delete-chats)                   | Delete multiple chats       | `request: DeleteChatsRequest`       |
| [`forward_message()`](#forward-message)             | Forward messages            | `request: ForwardMessageRequest`    |
| [`get_unseen_chat_count()`](#get-unseen-chat-count) | Get unseen chats count      | None                                |

## Bot Methods

| Method                                                  | Description                          | Parameters     |
|---------------------------------------------------------|--------------------------------------|----------------|
| [`get_webhook_info()`](#get-webhook-info)               | Get webhook info (GET)               | `token: str`   |
| [`get_webhook_info_post()`](#get-webhook-info-post)     | Get webhook info (POST)              | `token: str`   |
| [`log_out()`](#log-out)                                 | Log out bot (GET)                    | `token: str`   |
| [`log_out_post()`](#log-out-post)                       | Log out bot (POST)                   | `token: str`   |
| [`delete_webhook()`](#delete-webhook)                   | Delete webhook (GET)                 | `token: str`   |
| [`delete_webhook_post()`](#delete-webhook-post)         | Delete webhook (POST)                | `token: str`   |
| [`delete_webhook_delete()`](#delete-webhook-delete)     | Delete webhook (DELETE)              | `token: str`   |
| [`get_me()`](#get-me)                                   | Get bot information (GET)            | `token: str`   |
| [`get_me_post()`](#get-me-post)                         | Get bot information (POST)           | `token: str`   |

## Examples

### Basic Setup

```python
from basalam_sdk import BasalamClient, PersonalToken

auth = PersonalToken(
    token="your_access_token",
    refresh_token="your_refresh_token"
)
client = BasalamClient(auth=auth)
```

### Create Message

```python
import asyncio
from basalam_sdk.chat.models import MessageRequest, MessageTypeEnum, MessageInput

async def create_message_example():
    request = MessageRequest(
        chat_id=123,
        message_type=MessageTypeEnum.TEXT,
        content=MessageInput(
            text="Hello, how can I help you?"
        )
    )
    message = await client.chat.create_message(request=request)
    return message
```

### Create Chat

```python
import asyncio
from basalam_sdk.chat.models import CreateChatRequest

async def create_chat_example():
    request = CreateChatRequest(
        user_id=123
    )
    new_chat = await client.chat.create_chat(request=request)
    return new_chat
```

### Get Messages

```python
import asyncio
from basalam_sdk.chat.models import GetMessagesRequest

async def get_messages_example():
    request = GetMessagesRequest(
        chat_id=123,
        message_id=456,
        limit=20,
        order="desc",
    )
    messages = await client.chat.get_messages(request=request)

    # Option 2: With only some custom parameters
    messages = await client.chat.get_messages(
        request=GetMessagesRequest(chat_id=123, limit=50)
    )

    return messages
```

### Get Chats

```python
import asyncio
from basalam_sdk.chat.models import GetChatsRequest, MessageOrderByEnum, MessageFiltersEnum

async def get_chats_example():
    request = GetChatsRequest(
        limit=30,
        order_by=MessageOrderByEnum.UPDATED_AT,
        filters=MessageFiltersEnum.UNSEEN
    )
    chats = await client.chat.get_chats(request=request)
    return chats
```

### Edit Message

```python
import asyncio
from basalam_sdk.chat.models import EditMessageRequest, MessageInput

async def edit_message_example():
    request = EditMessageRequest(
        message_id=456,
        content=MessageInput(
            text="Updated message text"
        )
    )
    result = await client.chat.edit_message(request=request)
    return result
```

### Delete Message

```python
import asyncio
from basalam_sdk.chat.models import DeleteMessageRequest

async def delete_message_example():
    request = DeleteMessageRequest(
        message_ids=[456, 457]
    )
    result = await client.chat.delete_message(request=request)
    return result
```

### Delete Chats

```python
import asyncio
from basalam_sdk.chat.models import DeleteChatsRequest

async def delete_chats_example():
    request = DeleteChatsRequest(
        chat_ids=[123, 456, 789]
    )
    result = await client.chat.delete_chats(request=request)
    return result
```

### Forward Message

```python
import asyncio
from basalam_sdk.chat.models import ForwardMessageRequest

async def forward_message_example():
    request = ForwardMessageRequest(
        message_ids=[456, 457],
        chat_ids=[789]
    )
    result = await client.chat.forward_message(request=request)
    return result
```

### Get Unseen Chat Count

```python
import asyncio

async def get_unseen_chat_count_example():
    count = await client.chat.get_unseen_chat_count()
    print(f"Unseen chats: {count}")
    return count
```

### Get Webhook Info

```python
import asyncio

async def get_webhook_info_example():
    # Using GET method
    result = await client.chat.get_webhook_info(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    print(f"Webhook info: {result}")

    # Using POST method
    result = await client.chat.get_webhook_info_post(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result

# Synchronous version
def get_webhook_info_sync_example():
    result = client.chat.get_webhook_info_sync(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result
```

### Log Out Bot

```python
import asyncio

async def log_out_example():
    # Using GET method
    result = await client.chat.log_out(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    print(f"Log out result: {result}")

    # Using POST method
    result = await client.chat.log_out_post(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result

# Synchronous version
def log_out_sync_example():
    result = client.chat.log_out_sync(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result
```

### Delete Webhook

```python
import asyncio

async def delete_webhook_example():
    # Using GET method
    result = await client.chat.delete_webhook(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    print(f"Delete webhook result: {result}")

    # Using POST method
    result = await client.chat.delete_webhook_post(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )

    # Using DELETE method (recommended)
    result = await client.chat.delete_webhook_delete(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result

# Synchronous version
def delete_webhook_sync_example():
    result = client.chat.delete_webhook_sync(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result
```

### Get Me (Bot Information)

```python
import asyncio

async def get_me_example():
    # Using GET method
    result = await client.chat.get_me(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    print(f"Bot info: {result}")

    # Using POST method
    result = await client.chat.get_me_post(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result

# Synchronous version
def get_me_sync_example():
    result = client.chat.get_me_sync(
        token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )
    return result
```

## Message Types

The Chat Service supports various message types (see `MessageTypeEnum`):

- `file` - File attachments
- `product` - Product Card
- `vendor` - Vendor
- `text` - Plain text messages
- `picture` - Image messages (URL or file)
- `voice` - Audio messages
- `video` - Video messages
- `location` - Location sharing

## Next Steps

- [Order Service](./order.md) - Manage orders and payments
- [Upload Service](./upload.md) - File upload and management
- [Search Service](./search.md) - Search for products and entities 
