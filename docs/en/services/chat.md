# Chat Service

Handle messaging and chat functionalities with the Chat Service. This service provides comprehensive tools for managing
conversations, messages, and chat interactions: create and manage chat conversations, send and retrieve messages, handle
different message types, manage chat participants, and track chat history and updates.

## Table of Contents

- [Chat Methods](#chat-methods)
- [Examples](#examples)

## Chat Methods

| Method                                              | Description                 | Parameters                                                     |
|-----------------------------------------------------|-----------------------------|----------------------------------------------------------------|
| [`create_message()`](#create-message)               | Create a message            | `chat_id: int, request: MessageRequest`                        |
| [`create_chat()`](#create-chat)                     | Create a chat               | `request: CreateChatRequest`                                   |
| [`get_messages()`](#get-messages)                   | Get chat messages           | `chat_id: int, request: Optional[GetMessagesRequest] = None`   |
| [`get_chats()`](#get-chats)                         | Get chats list              | `request: GetChatsRequest`                                     |
| [`edit_message()`](#edit-message)                   | Edit an existing message    | `chat_id: int, message_id: int, request: EditMessageRequest`   |
| [`delete_message()`](#delete-message)               | Delete a message            | `chat_id: int, message_id: int`                                |
| [`delete_chats()`](#delete-chats)                   | Delete multiple chats       | `request: DeleteChatsRequest`                                  |
| [`forward_message()`](#forward-message)             | Forward a message           | `chat_id: int, request: ForwardMessageRequest`                 |
| [`get_unseen_chat_count()`](#get-unseen-chat-count) | Get unseen chats count      | None                                                           |

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
    message = await client.chat.create_message(chat_id=123, request=request)
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
        message_id=456,
        limit=20,
        order="desc",
    )
    messages = await client.chat.get_messages(chat_id=123, request=request)

    # Option 2: With default parameters (request is optional)
    messages = await client.chat.get_messages(chat_id=123)

    # Option 3: With only some custom parameters
    messages = await client.chat.get_messages(
        chat_id=123,
        request=GetMessagesRequest(limit=50)
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
from basalam_sdk.chat.models import EditMessageRequest

async def edit_message_example():
    request = EditMessageRequest(
        text="Updated message text"
    )
    result = await client.chat.edit_message(
        chat_id=123,
        message_id=456,
        request=request
    )
    return result
```

### Delete Message

```python
import asyncio

async def delete_message_example():
    result = await client.chat.delete_message(
        chat_id=123,
        message_id=456
    )
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
        message_id=[456, 457],
        chat_ids=[789]
    )
    result = await client.chat.forward_message(
        chat_id=123,
        request=request
    )
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
