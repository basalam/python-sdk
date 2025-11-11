"""
Client for the Chat service API.
"""
from typing import Optional

from .models import (
    MessageRequest,
    CreateChatRequest,
    ChatListResponse,
    MessageResponse,
    CreateChatResponse,
    GetMessagesRequest,
    GetMessagesResponse,
    GetChatsRequest,
    EditMessageRequest,
    EditMessageResponse,
    DeleteMessageRequest,
    DeleteChatsRequest,
    ForwardMessageRequest,
    BooleanResponse,
    UnseenChatCountResponse,
    BotApiResponse
)
from ..base_client import BaseClient


class ChatService(BaseClient):
    """Client for the Chat service API."""

    def __init__(self, **kwargs):
        """Initialize the chat service client."""
        super().__init__(service="chat", **kwargs)

    async def create_message(
            self,
            request: MessageRequest,
            user_agent: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> MessageResponse:
        """
        Create a message.

        Args:
            request: The message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.

        Returns:
            MessageResponse: The response from the API.
        """
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        endpoint = f"/v1/chats/{request.chat_id}/messages"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return MessageResponse(**response)

    def create_message_sync(
            self,
            request: MessageRequest,
            user_agent: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> MessageResponse:
        """
        Create a message (synchronous version).

        Args:
            request: The message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.

        Returns:
            MessageResponse: The response from the API.
        """
        endpoint = f"/v1/chats/{request.chat_id}/messages"
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return MessageResponse(**response)

    async def create_chat(
            self,
            request: CreateChatRequest,
            x_creation_tags: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_user_session: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None  # Just for Basalam internal team usage!!!
    ) -> CreateChatResponse:
        """
        Create a private chat.

        Args:
            request: The create chat request model.
            x_creation_tags: Optional X-Creation-Tags header value.
            x_user_session: Optional X-User-Session header value.
            x_client_info: Optional X-Client-Info header value.

        Returns:
            CreateChatResponse: The response from the API.
        """
        endpoint = "/v1/chats"
        headers = {}
        if x_creation_tags:
            headers["X-Creation-Tags"] = x_creation_tags
        if x_user_session:
            headers["X-User-Session"] = x_user_session
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return CreateChatResponse(**response)

    def create_chat_sync(
            self,
            request: CreateChatRequest,
            x_creation_tags: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_user_session: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None  # Just for Basalam internal team usage!!!
    ) -> CreateChatResponse:
        """
        Create a private chat (synchronous version).

        Args:
            request: The create chat request model.
            x_creation_tags: Optional X-Creation-Tags header value.
            x_user_session: Optional X-User-Session header value.
            x_client_info: Optional X-Client-Info header value.

        Returns:
            CreateChatResponse: The response from the API.
        """
        endpoint = "/v1/chats"
        headers = {}
        if x_creation_tags:
            headers["X-Creation-Tags"] = x_creation_tags
        if x_user_session:
            headers["X-User-Session"] = x_user_session
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return CreateChatResponse(**response)

    async def get_messages(
            self,
            request: Optional[GetMessagesRequest] = None,
    ) -> GetMessagesResponse:
        """
        Get messages from a chat.

        Args:
            request: Optional request model containing query parameters (limit, order, cmp, message_id).

        Returns:
            GetMessagesResponse: The response containing the list of messages.
        """
        endpoint = f"/v1/chats/{request.chat_id}/messages"
        params = {
            "limit": request.limit,
            "order": request.order,
            "cmp": request.cmp
        }
        if request.message_id is not None:
            params["message_id"] = request.message_id

        response = await self._get(endpoint, params=params)
        return GetMessagesResponse(**response)

    def get_messages_sync(
            self,
            request: Optional[GetMessagesRequest] = None,
    ) -> GetMessagesResponse:
        """
        Get messages from a chat (synchronous version).

        Args:
            request: Optional request model containing query parameters (limit, order, cmp, message_id).

        Returns:
            GetMessagesResponse: The response containing the list of messages.
        """
        endpoint = f"/v1/chats/{request.chat_id}/messages"
        params = {
            "limit": request.limit,
            "order": request.order,
            "cmp": request.cmp
        }
        if request.message_id is not None:
            params["message_id"] = request.message_id

        response = self._get_sync(endpoint, params=params)
        return GetMessagesResponse(**response)

    async def get_chats(
            self,
            request: GetChatsRequest,
    ) -> ChatListResponse:
        """
        Get list of chats.

        Args:
            request: The get chats request model containing query parameters.

        Returns:
            ChatListResponse: The list of chats.
        """
        params = {
            "limit": request.limit,
            "order_by": request.order_by.value
        }
        if request.updated_from is not None:
            params["updated_from"] = request.updated_from
        if request.updated_before is not None:
            params["updated_before"] = request.updated_before
        if request.modified_from is not None:
            params["modified_from"] = request.modified_from
        if request.modified_before is not None:
            params["modified_before"] = request.modified_before
        if request.filters is not None:
            params["filters"] = request.filters.value

        endpoint = f"/v1/chats"
        response = await self._get(endpoint, params=params)
        return ChatListResponse(**response)

    def get_chats_sync(
            self,
            request: GetChatsRequest,
    ) -> ChatListResponse:
        """
        Get list of chats (synchronous version).

        Args:
            request: The get chats request model containing query parameters.

        Returns:
            ChatListResponse: The list of chats.
        """
        params = {
            "limit": request.limit,
            "order_by": request.order_by.value
        }
        if request.updated_from is not None:
            params["updated_from"] = request.updated_from
        if request.updated_before is not None:
            params["updated_before"] = request.updated_before
        if request.modified_from is not None:
            params["modified_from"] = request.modified_from
        if request.modified_before is not None:
            params["modified_before"] = request.modified_before
        if request.filters is not None:
            params["filters"] = request.filters.value

        endpoint = f"/v1/chats"
        response = self._get_sync(endpoint, params=params)
        return ChatListResponse(**response)

    async def edit_message(
            self,
            request: EditMessageRequest,
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> EditMessageResponse:
        """
        Edit a message.

        Args:
            request: The edit message request model.
            x_client_info: The X-Client-Info header value.

        Returns:
            EditMessageResponse: The response from the API.
        """
        headers = {}
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        endpoint = "/v1/chats/messages"
        response = await self._patch(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return EditMessageResponse(**response)

    def edit_message_sync(
            self,
            request: EditMessageRequest,
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> EditMessageResponse:
        """
        Edit a message (synchronous version).

        Args:
            request: The edit message request model.
            x_client_info: The X-Client-Info header value.

        Returns:
            EditMessageResponse: The response from the API.
        """
        headers = {}
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        endpoint = "/v1/chats/messages"
        response = self._patch_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return EditMessageResponse(**response)

    async def delete_message(
            self,
            request: DeleteMessageRequest,
    ) -> BooleanResponse:
        """
        Delete messages.

        Args:
            request: The delete message request model containing message IDs.

        Returns:
            BooleanResponse: The response from the API.
        """
        endpoint = "/v1/chats/messages"
        response = await self._delete(endpoint, json_data=request.model_dump(exclude_none=True))
        return BooleanResponse(**response)

    def delete_message_sync(
            self,
            request: DeleteMessageRequest,
    ) -> BooleanResponse:
        """
        Delete messages (synchronous version).

        Args:
            request: The delete message request model containing message IDs.

        Returns:
            BooleanResponse: The response from the API.
        """
        endpoint = "/v1/chats/messages"
        response = self._delete_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return BooleanResponse(**response)

    async def delete_chats(
            self,
            request: DeleteChatsRequest,
    ) -> BooleanResponse:
        """
        Delete chats.

        Args:
            request: The delete chats request model containing chat IDs.

        Returns:
            BooleanResponse: The response from the API.
        """
        endpoint = "/v1/chats"
        response = await self._delete(endpoint, json_data=request.model_dump(exclude_none=True))
        return BooleanResponse(**response)

    def delete_chats_sync(
            self,
            request: DeleteChatsRequest,
    ) -> BooleanResponse:
        """
        Delete chats (synchronous version).

        Args:
            request: The delete chats request model containing chat IDs.

        Returns:
            BooleanResponse: The response from the API.
        """
        endpoint = "/v1/chats"
        response = self._delete_sync(endpoint, json_data=request.model_dump(exclude_none=True))
        return BooleanResponse(**response)

    async def forward_message(
            self,
            request: ForwardMessageRequest,
            user_agent: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> BooleanResponse:
        """
        Forward messages to multiple conversations.

        Args:
            request: The forward message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.

        Returns:
            BooleanResponse: The response from the API.
        """
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        endpoint = "/v1/chats/messages/forward"
        response = await self._post(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return BooleanResponse(**response)

    def forward_message_sync(
            self,
            request: ForwardMessageRequest,
            user_agent: Optional[str] = None,  # Just for Basalam internal team usage!!!
            x_client_info: Optional[str] = None,  # Just for Basalam internal team usage!!!
    ) -> BooleanResponse:
        """
        Forward messages to multiple conversations (synchronous version).

        Args:
            request: The forward message request model.
            user_agent: The User-Agent header value.
            x_client_info: The X-Client-Info header value.

        Returns:
            BooleanResponse: The response from the API.
        """
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        if x_client_info:
            headers["X-Client-Info"] = x_client_info

        endpoint = "/v1/chats/messages/forward"
        response = self._post_sync(endpoint, json_data=request.model_dump(exclude_none=True), headers=headers)
        return BooleanResponse(**response)

    async def get_unseen_chat_count(self) -> UnseenChatCountResponse:
        """
        Get unseen chat count.

        Returns:
            UnseenChatCountResponse: The response containing count and more_than_count flag.
        """
        endpoint = "/v1/chats/unseen-count"
        response = await self._get(endpoint)
        return UnseenChatCountResponse(**response)

    def get_unseen_chat_count_sync(self) -> UnseenChatCountResponse:
        """
        Get unseen chat count (synchronous version).

        Returns:
            UnseenChatCountResponse: The response containing count and more_than_count flag.
        """
        endpoint = "/v1/chats/unseen-count"
        response = self._get_sync(endpoint)
        return UnseenChatCountResponse(**response)

    async def get_webhook_info(self, token: str) -> BotApiResponse:
        """
        Get webhook information for the bot (GET method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing webhook information.
        """
        endpoint = f"/v1/bots/{token}/getWebhookInfo"
        response = await self._get(endpoint)
        return BotApiResponse(**response)

    def get_webhook_info_sync(self, token: str) -> BotApiResponse:
        """
        Get webhook information for the bot (GET method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing webhook information.
        """
        endpoint = f"/v1/bots/{token}/getWebhookInfo"
        response = self._get_sync(endpoint)
        return BotApiResponse(**response)

    async def get_webhook_info_post(self, token: str) -> BotApiResponse:
        """
        Get webhook information for the bot (POST method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing webhook information.
        """
        endpoint = f"/v1/bots/{token}/getWebhookInfo"
        response = await self._post(endpoint)
        return BotApiResponse(**response)

    def get_webhook_info_post_sync(self, token: str) -> BotApiResponse:
        """
        Get webhook information for the bot (POST method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing webhook information.
        """
        endpoint = f"/v1/bots/{token}/getWebhookInfo"
        response = self._post_sync(endpoint)
        return BotApiResponse(**response)

    async def log_out(self, token: str) -> BotApiResponse:
        """
        Log out the bot and invalidate its token (GET method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/logOut"
        response = await self._get(endpoint)
        return BotApiResponse(**response)

    def log_out_sync(self, token: str) -> BotApiResponse:
        """
        Log out the bot and invalidate its token (GET method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/logOut"
        response = self._get_sync(endpoint)
        return BotApiResponse(**response)

    async def log_out_post(self, token: str) -> BotApiResponse:
        """
        Log out the bot and invalidate its token (POST method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/logOut"
        response = await self._post(endpoint)
        return BotApiResponse(**response)

    def log_out_post_sync(self, token: str) -> BotApiResponse:
        """
        Log out the bot and invalidate its token (POST method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/logOut"
        response = self._post_sync(endpoint)
        return BotApiResponse(**response)

    async def delete_webhook(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (GET method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = await self._get(endpoint)
        return BotApiResponse(**response)

    def delete_webhook_sync(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (GET method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = self._get_sync(endpoint)
        return BotApiResponse(**response)

    async def delete_webhook_post(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (POST method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = await self._post(endpoint)
        return BotApiResponse(**response)

    def delete_webhook_post_sync(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (POST method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = self._post_sync(endpoint)
        return BotApiResponse(**response)

    async def delete_webhook_delete(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (DELETE method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = await self._delete(endpoint)
        return BotApiResponse(**response)

    def delete_webhook_delete_sync(self, token: str) -> BotApiResponse:
        """
        Delete the webhook URL for the bot (DELETE method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response from the API.
        """
        endpoint = f"/v1/bots/{token}/deleteWebhook"
        response = self._delete_sync(endpoint)
        return BotApiResponse(**response)

    async def get_me(self, token: str) -> BotApiResponse:
        """
        Get information about the bot (GET method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing bot information.
        """
        endpoint = f"/v1/bots/{token}/getMe"
        response = await self._get(endpoint)
        return BotApiResponse(**response)

    def get_me_sync(self, token: str) -> BotApiResponse:
        """
        Get information about the bot (GET method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing bot information.
        """
        endpoint = f"/v1/bots/{token}/getMe"
        response = self._get_sync(endpoint)
        return BotApiResponse(**response)

    async def get_me_post(self, token: str) -> BotApiResponse:
        """
        Get information about the bot (POST method).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing bot information.
        """
        endpoint = f"/v1/bots/{token}/getMe"
        response = await self._post(endpoint)
        return BotApiResponse(**response)

    def get_me_post_sync(self, token: str) -> BotApiResponse:
        """
        Get information about the bot (POST method, synchronous version).

        Args:
            token: The bot token.

        Returns:
            BotApiResponse: The response containing bot information.
        """
        endpoint = f"/v1/bots/{token}/getMe"
        response = self._post_sync(endpoint)
        return BotApiResponse(**response)
