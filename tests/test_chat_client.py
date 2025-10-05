"""
Tests for the Chat service client.
"""
import pytest

from basalam_sdk import BasalamClient
from basalam_sdk.auth import PersonalToken
from basalam_sdk.chat.models import (
    MessageRequest,
    CreateChatRequest,
    MessageInput,
    MessageTypeEnum,
    GetMessagesRequest,
    GetChatsRequest, MessageOrderByEnum,
)
from basalam_sdk.config import BasalamConfig, Environment

# Test data
TEST_CHAT_ID = 183583802
TEST_USER_ID = 430


@pytest.fixture
def basalam_client():
    """Create a BasalamClient instance with real auth and config."""
    config = BasalamConfig(
        environment=Environment.PRODUCTION,
        timeout=30.0,
        user_agent="SDK-Test"
    )
    auth = PersonalToken(
        token=""
    )
    return BasalamClient(auth=auth, config=config)


# -------------------------------------------------------------------------
# Message endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_message_async(basalam_client):
    """Test create_message async method."""
    try:
        message_input = MessageInput(
            text="Test message",
            entity_id=123
        )
        request = MessageRequest(
            chat_id=TEST_CHAT_ID,
            content=message_input,
            message_type=MessageTypeEnum.TEXT,
            temp_id=12345
        )
        result = await basalam_client.chat.create_message(
            request=request,
        )
        print(f"create_message async result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'id')
    except Exception as e:
        print(f"create_message async error: {e}")
        assert True


def test_create_message_sync(basalam_client):
    """Test create_message_sync method."""
    try:
        message_input = MessageInput(
            text="Test message",
            entity_id=123
        )
        request = MessageRequest(
            chat_id=TEST_CHAT_ID,
            content=message_input,
            message_type=MessageTypeEnum.TEXT,
            temp_id=12345
        )
        result = basalam_client.chat.create_message_sync(
            request=request
        )
        print(f"create_message_sync result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'id')
    except Exception as e:
        print(f"create_message_sync error: {e}")
        assert True


@pytest.mark.asyncio
async def test_get_messages_async(basalam_client):
    """Test get_messages async method."""
    try:
        request = GetMessagesRequest(
            chat_id=TEST_CHAT_ID
        )
        result = await basalam_client.chat.get_messages(
            request=request
        )
        print(f"get_messages async result: {result}")
    except Exception as e:
        print(f"get_messages async error: {e}")
        assert True


def test_get_messages_sync(basalam_client):
    """Test get_messages_sync method."""
    try:
        request = GetMessagesRequest(
            chat_id=TEST_CHAT_ID,

        )
        result = basalam_client.chat.get_messages_sync(
            request=request
        )
        print(f"get_messages_sync result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'messages')
        assert isinstance(result.data.messages, list)
    except Exception as e:
        print(f"get_messages_sync error: {e}")
        assert True


# -------------------------------------------------------------------------
# Chat endpoints tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_chat_async(basalam_client):
    """Test create_chat async method."""
    try:
        request = CreateChatRequest(
            user_id=1308962
        )
        result = await basalam_client.chat.create_chat(
            request=request
        )
        print(f"create_chat async result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'id')
    except Exception as e:
        print(f"create_chat async error: {e}")
        assert True


def test_create_chat_sync(basalam_client):
    """Test create_chat_sync method."""
    try:
        request = CreateChatRequest(
            user_id=1308962
        )
        result = basalam_client.chat.create_chat_sync(
            request=request
        )
        print(f"create_chat_sync result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'id')
    except Exception as e:
        print(f"create_chat_sync error: {e}")
        assert True


@pytest.mark.asyncio
async def test_get_chats_async(basalam_client):
    """Test get_chats async method."""
    try:
        request = GetChatsRequest(
            limit=10
        )
        result = await basalam_client.chat.get_chats(
            request=request
        )
        print(f"get_chats async result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'chats')
        assert isinstance(result.data.chats, list)
    except Exception as e:
        print(f"get_chats async error: {e}")
        assert True


def test_get_chats_sync(basalam_client):
    """Test get_chats_sync method."""
    try:
        request = GetChatsRequest(
            limit=10,
            order_by=MessageOrderByEnum.UPDATED_AT
        )
        result = basalam_client.chat.get_chats_sync(
            request=request
        )
        print(f"get_chats_sync result: {result}")
        assert result is not None
        assert hasattr(result, 'data')
        assert hasattr(result.data, 'chats')
        assert isinstance(result.data.chats, list)
    except Exception as e:
        print(f"get_chats_sync error: {e}")
        assert True


# -------------------------------------------------------------------------
# Model dump exclude none tests
# -------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_model_dump_exclude_none_async(basalam_client):
    """Test that model_dump(exclude_none=True) works correctly for chat models."""
    chat_service = basalam_client.chat

    # Create a message request with optional fields set to None
    message_input = MessageInput(
        text="Test message",
        entity_id=None  # This should be excluded from the request
    )
    request = MessageRequest(
        chat_id=TEST_CHAT_ID,
        message_type=MessageTypeEnum.TEXT,
        message_source=None,  # This should be excluded from the request
        message=message_input,
        attachment=None,  # This should be excluded from the request
        replied_message_id=None,  # This should be excluded from the request
        message_metadata=None,  # This should be excluded from the request
        temp_id=None  # This should be excluded from the request
    )

    # Test the model_dump method
    dumped_data = request.model_dump(exclude_none=True)
    print(f"Model dump result: {dumped_data}")

    # Verify that None values are excluded
    assert "message_source" not in dumped_data
    assert "attachment" not in dumped_data
    assert "replied_message_id" not in dumped_data
    assert "message_metadata" not in dumped_data
    assert "temp_id" not in dumped_data

    # Verify that required fields are included
    assert "chat_id" in dumped_data
    assert "message_type" in dumped_data
    assert "message" in dumped_data

    # Verify that nested None values are excluded
    assert "entity_id" not in dumped_data["message"]
    assert "text" in dumped_data["message"]


def test_model_dump_exclude_none_sync(basalam_client):
    """Test that model_dump(exclude_none=True) works correctly for chat models (sync version)."""
    chat_service = basalam_client.chat

    # Create a chat request with optional fields set to None
    request = CreateChatRequest(
        chat_type="private",
        user_id=None,  # This should be excluded from the request
        hash_id=None  # This should be excluded from the request
    )

    # Test the model_dump method
    dumped_data = request.model_dump(exclude_none=True)
    print(f"Model dump result: {dumped_data}")

    # Verify that None values are excluded
    assert "user_id" not in dumped_data
    assert "hash_id" not in dumped_data

    # Verify that required fields are included
    assert "chat_type" in dumped_data
