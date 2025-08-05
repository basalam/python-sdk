# Chat Service

Handle messaging and chat functionalities with the Chat Service. This service provides comprehensive tools for managing
conversations, messages, and chat interactions: create and manage chat conversations, send and retrieve messages, handle
different message types, manage chat participants, and track chat history and updates.

## Table of Contents

- [Chat Methods](#chat-methods)
- [Examples](#examples)

## Chat Methods

| Method                                | Description       | Parameters                    |
|---------------------------------------|-------------------|-------------------------------|
| [`create_message()`](#create-message) | Create a message  | `request: MessageRequest`     |
| [`create_chat()`](#create-chat)       | Create a chat     | `request: CreateChatRequest`  |
| [`get_messages()`](#get-messages)     | Get chat messages | `request: GetMessagesRequest` |
| [`get_chats()`](#get-chats)           | Get chats list    | `request: GetChatsRequest`    |

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
    message = await client.create_message(request=request)
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
    new_chat = await client.create_chat(request=request)
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
    messages = await client.get_messages(request=request)
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
    chats = await client.get_chats(request=request)
    return chats
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
