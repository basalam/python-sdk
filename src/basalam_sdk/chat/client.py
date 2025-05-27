"""
Client for the Chat service API.
"""
from typing import Dict, Any, Optional

from .models import MessageRequestModel, CreateChatRequest
from ..base_client import BaseClient


class ChatService(BaseClient):
    """Client for the Chat service API."""

    def __init__(self, **kwargs):
        """Initialize the chat service client."""
        super().__init__(service_name="chat", **kwargs)

    async def send_message(
            self,
            request: MessageRequestModel,
            user_agent: str,
            x_client_info: str,
            admin_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a message.

        Args:
            request: The message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.
            admin_token: Optional Admin-Token header value.

        Returns:
            The response from the API.
        """
        endpoint = "/v2/message"
        headers = {
            "User-Agent": user_agent,
            "X-Client-Info": x_client_info
        }
        if admin_token:
            headers["Admin-Token"] = admin_token

        response = await self._post(endpoint, json=request.dict(), headers=headers)
        return response

    def send_message_sync(
            self,
            request: MessageRequestModel,
            user_agent: str,
            x_client_info: str,
            admin_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a message (synchronous version).

        Args:
            request: The message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.
            admin_token: Optional Admin-Token header value.

        Returns:
            The response from the API.
        """
        endpoint = "/v2/message"
        headers = {
            "User-Agent": user_agent,
            "X-Client-Info": x_client_info
        }
        if admin_token:
            headers["Admin-Token"] = admin_token

        response = self._post_sync(endpoint, json=request.dict(), headers=headers)
        return response

    async def create_chat(
            self,
            request: CreateChatRequest,
            x_creation_tags: Optional[str] = None,
            x_user_session: Optional[str] = None,
            x_client_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a private chat.

        Args:
            request: The create chat request model.
            x_creation_tags: Optional X-Creation-Tags header value.
            x_user_session: Optional X-User-Session header value.
            x_client_info: Optional X-Client-Info header value.

        Returns:
            The response from the API.
        """
        endpoint = "/v2/chat"
        headers = {}
        if x_creation_tags:
            headers["X-Creation-Tags"] = x_creation_tags
        if x_user_session:
            headers["X-User-Session"] = x_user_session
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        response = await self._post(endpoint, json=request.dict(), headers=headers)
        return response

    def create_chat_sync(
            self,
            request: CreateChatRequest,
            x_creation_tags: Optional[str] = None,
            x_user_session: Optional[str] = None,
            x_client_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a private chat (synchronous version).

        Args:
            request: The create chat request model.
            x_creation_tags: Optional X-Creation-Tags header value.
            x_user_session: Optional X-User-Session header value.
            x_client_info: Optional X-Client-Info header value.

        Returns:
            The response from the API.
        """
        endpoint = "/v2/chat"
        headers = {}
        if x_creation_tags:
            headers["X-Creation-Tags"] = x_creation_tags
        if x_user_session:
            headers["X-User-Session"] = x_user_session
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        response = self._post_sync(endpoint, json=request.dict(), headers=headers)
        return response

    async def get_messages(
            self,
            chat_id: int,
            msg_id: Optional[int] = None,
            limit: int = 20,
            chat_type: str = "ALL",
            order: str = "DESC",
            op: str = "<",
            temp_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get messages from a chat.

        Args:
            chat_id: The ID of the chat.
            msg_id: Optional message ID to start from.
            limit: Maximum number of messages to return.
            chat_type: Type of chat messages to return.
            order: Order of messages (ASC or DESC).
            op: Operator for message ID comparison.
            temp_id: Optional temporary message ID.

        Returns:
            The response from the API.
        """
        endpoint = f"/v2/chat/{chat_id}/messages"
        params = {
            "limit": limit,
            "chatType": chat_type,
            "order": order,
            "op": op
        }
        if msg_id is not None:
            params["msgId"] = msg_id
        if temp_id is not None:
            params["temp_id"] = temp_id

        response = await self._get(endpoint, params=params)
        return response

    def get_messages_sync(
            self,
            chat_id: int,
            msg_id: Optional[int] = None,
            limit: int = 20,
            chat_type: str = "ALL",
            order: str = "DESC",
            op: str = "<",
            temp_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get messages from a chat (synchronous version).

        Args:
            chat_id: The ID of the chat.
            msg_id: Optional message ID to start from.
            limit: Maximum number of messages to return.
            chat_type: Type of chat messages to return.
            order: Order of messages (ASC or DESC).
            op: Operator for message ID comparison.
            temp_id: Optional temporary message ID.

        Returns:
            The response from the API.
        """
        endpoint = f"/v2/chat/{chat_id}/messages"
        params = {
            "limit": limit,
            "chatType": chat_type,
            "order": order,
            "op": op
        }
        if msg_id is not None:
            params["msgId"] = msg_id
        if temp_id is not None:
            params["temp_id"] = temp_id

        response = self._get_sync(endpoint, params=params)
        return response
