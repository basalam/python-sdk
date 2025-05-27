"""
Authentication module for the Basalam SDK.

This module provides authentication classes for different OAuth2 flows.
It supports both synchronous and asynchronous operations with comprehensive error handling.

Available authentication methods:
- ClientCredentials: For server-to-server API calls
- AuthorizationCode: For user-authorized applications

For more information, see:
- https://developers.basalam.com/authorization
- https://developers.basalam.com/scopes
"""
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Union
from urllib.parse import urlencode

import httpx

from .config import BasalamConfig
from .errors import BasalamAuthError


class Scope(str, Enum):
    """
    Available OAuth scopes for Basalam API.

    See https://developers.basalam.com/scopes for more details.
    """
    # Order processing
    ORDER_PROCESSING = "order-processing"

    # Vendor profile scopes
    VENDOR_PROFILE_READ = "vendor.profile.read"
    VENDOR_PROFILE_WRITE = "vendor.profile.write"

    # Customer profile scopes
    CUSTOMER_PROFILE_READ = "customer.profile.read"
    CUSTOMER_PROFILE_WRITE = "customer.profile.write"

    # Vendor product scopes
    VENDOR_PRODUCT_READ = "vendor.product.read"
    VENDOR_PRODUCT_WRITE = "vendor.product.write"

    # Customer order scopes
    CUSTOMER_ORDER_READ = "customer.order.read"
    CUSTOMER_ORDER_WRITE = "customer.order.write"

    # Vendor parcel scopes
    VENDOR_PARCEL_READ = "vendor.parcel.read"
    VENDOR_PARCEL_WRITE = "vendor.parcel.write"

    # Customer wallet scopes
    CUSTOMER_WALLET_READ = "customer.wallet.read"
    CUSTOMER_WALLET_WRITE = "customer.wallet.write"

    # Customer chat scopes
    CUSTOMER_CHAT_READ = "customer.chat.read"
    CUSTOMER_CHAT_WRITE = "customer.chat.write"

    @classmethod
    def get_entity_scopes(cls, entity: str) -> Set[str]:
        """
        Get all scopes for a specific entity.
        """
        return {scope.value for scope in cls if scope.value.startswith(f"{entity}.")}

    @classmethod
    def get_read_scopes(cls) -> Set[str]:
        """
        Get all read scopes.
        """
        return {scope.value for scope in cls if scope.value.endswith(".read")}

    @classmethod
    def get_write_scopes(cls) -> Set[str]:
        """
        Get all write scopes.
        """
        return {scope.value for scope in cls if scope.value.endswith(".write")}

    @classmethod
    def get_feature_scopes(cls, feature: str) -> Set[str]:
        """
        Get all scopes for a specific feature.
        """
        return {scope.value for scope in cls if f".{feature}." in scope.value}


@dataclass
class TokenInfo:
    """
    Token information container.
    """
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: float = None

    def __post_init__(self):
        """Initialize created_at if not provided."""
        if self.created_at is None:
            self.created_at = time.time()

    @property
    def expires_at(self) -> float:
        """Get the expiration timestamp."""
        return self.created_at + self.expires_in

    @property
    def is_expired(self) -> bool:
        """Check if the token is expired."""
        return time.time() >= self.expires_at

    @property
    def should_refresh(self) -> bool:
        """Check if the token should be refreshed (expires in less than 5 minutes)."""
        return time.time() >= (self.expires_at - 300)  # 300 seconds = 5 minutes

    @property
    def granted_scopes(self) -> Set[str]:
        """Get the set of granted scopes from the token."""
        if not self.scope:
            return set()
        return set(self.scope.split())

    def has_scope(self, scope: Union[str, Scope]) -> bool:
        """
        Check if the token has a specific scope.
        """
        scope_value = scope.value if isinstance(scope, Scope) else scope
        return scope_value in self.granted_scopes


class BaseAuth(ABC):
    """
    Base authentication class for Basalam API.

    This abstract class defines the interface for all authentication methods.
    """

    def __init__(self, config: Optional[BasalamConfig] = None):
        """
        Initialize authentication with optional configuration.
        """
        self.config = config or BasalamConfig()
        self._token_info: Optional[TokenInfo] = None

    @property
    def token_info(self) -> Optional[TokenInfo]:
        """Get the current token information."""
        return self._token_info

    @abstractmethod
    async def get_token(self) -> TokenInfo:
        """
        Get a token asynchronously.
        """
        pass

    @abstractmethod
    def get_token_sync(self) -> TokenInfo:
        """
        Get a token synchronously.
        """
        pass

    @abstractmethod
    async def refresh_token(self) -> TokenInfo:
        """
        Refresh the token asynchronously.
        """
        pass

    @abstractmethod
    def refresh_token_sync(self) -> TokenInfo:
        """
        Refresh the token synchronously.
        """
        pass

    async def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests asynchronously.
        """
        if not self._token_info or self._token_info.should_refresh:
            self._token_info = await self.refresh_token() if self._token_info else await self.get_token()
        return {"Authorization": f"{self._token_info.token_type} {self._token_info.access_token}"}

    def get_auth_headers_sync(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests synchronously.
        """
        if not self._token_info or self._token_info.should_refresh:
            self._token_info = self.refresh_token_sync() if self._token_info else self.get_token_sync()
        return {"Authorization": f"{self._token_info.token_type} {self._token_info.access_token}"}

    def get_granted_scopes(self) -> Set[str]:
        """
        Get the set of granted scopes from the token.
        """
        if not self._token_info:
            return set()
        return self._token_info.granted_scopes

    def has_scope(self, scope: Union[str, Scope]) -> bool:
        """
        Check if the token has a specific scope.
        """
        if not self._token_info:
            return False
        return self._token_info.has_scope(scope)

    def validate_scopes(self, required_scopes: List[Union[str, Scope]]) -> None:
        """
        Validate that the token has all required scopes.
        """
        if not self._token_info:
            raise BasalamAuthError("No token available")

        missing_scopes = []
        for scope in required_scopes:
            if not self.has_scope(scope):
                scope_value = scope.value if isinstance(scope, Scope) else scope
                missing_scopes.append(scope_value)

        if missing_scopes:
            raise BasalamAuthError(
                f"Missing required scopes: {', '.join(missing_scopes)}"
            )


class ClientCredentials(BaseAuth):
    """
    Client credentials authentication flow.

    This authentication method is suitable for server-to-server API calls
    where user authorization is not needed.

    For detailed examples, see: docs/client_credentials_example.md
    """

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            scopes: Optional[Union[str, List[Union[str, Scope]]]] = '*',
            config: Optional[BasalamConfig] = None,
    ):
        """
        Initialize client credentials authentication.
        """
        super().__init__(config)
        self.client_id = client_id
        self.client_secret = client_secret

        # Handle scope formatting
        if isinstance(scopes, list):
            scope_values = []
            for s in scopes:
                if isinstance(s, Scope):
                    scope_values.append(s.value)
                else:
                    scope_values.append(s)
            self.scope = " ".join(scope_values)
        else:
            self.scope = scopes

    async def get_token(self) -> TokenInfo:
        """
        Get an access token using client credentials flow asynchronously.
        """
        if self._token_info and not self._token_info.should_refresh:
            return self._token_info

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.scope
            }

            try:
                response = await client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token"),
                    scope=token_data.get("scope", self.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to get access token: {str(e)}")

    def get_token_sync(self) -> TokenInfo:
        """
        Get an access token using client credentials flow synchronously.
        """
        if self._token_info and not self._token_info.should_refresh:
            return self._token_info

        with httpx.Client(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": self.scope
            }

            try:
                response = client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token"),
                    scope=token_data.get("scope", self.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to get access token: {str(e)}")

    async def refresh_token(self) -> TokenInfo:
        """
        Refresh the access token asynchronously.

        Note: Unlike Authorization Code flow, Client Credentials flow doesn't use refresh tokens.
        This method simply gets a new access token using the client credentials.
        """
        # Client Credentials flow doesn't use refresh tokens - just get a new token
        return await self.get_token()

    def refresh_token_sync(self) -> TokenInfo:
        """
        Refresh the access token synchronously.

        Note: Unlike Authorization Code flow, Client Credentials flow doesn't use refresh tokens.
        This method simply gets a new access token using the client credentials.
        """
        # Client Credentials flow doesn't use refresh tokens - just get a new token
        return self.get_token_sync()


class AuthorizationCode(BaseAuth):
    """
    Authorization code authentication flow.

    This authentication method is suitable for applications that need
    to access resources on behalf of a user.

    For detailed examples, see: docs/authorization_code_example.md
    """

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            redirect_uri: str,
            scopes: Optional[Union[str, List[Union[str, Scope]]]] = None,
            config: Optional[BasalamConfig] = None,
    ):
        """
        Initialize authorization code flow.
        """
        super().__init__(config)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # Handle scope formatting
        if isinstance(scopes, list):
            scope_values = []
            for s in scopes:
                if isinstance(s, Scope):
                    scope_values.append(s.value)
                else:
                    scope_values.append(s)
            self.scope = " ".join(scope_values)
        else:
            self.scope = scopes

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Get the authorization URL for the user to visit.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri
        }

        if self.scope:
            params["scope"] = self.scope

        if state:
            params["state"] = state

        # Build the URL
        return f"{self.config.authorize_url}?{urlencode(params)}"

    async def exchange_code(self, code: str) -> TokenInfo:
        """
        Exchange an authorization code for an access token asynchronously.
        """
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }

            try:
                response = await client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token"),
                    scope=token_data.get("scope", self.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to exchange authorization code: {str(e)}")

    def exchange_code_sync(self, code: str) -> TokenInfo:
        """
        Exchange an authorization code for an access token synchronously.
        """
        with httpx.Client(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }

            try:
                response = client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    refresh_token=token_data.get("refresh_token"),
                    scope=token_data.get("scope", self.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to exchange authorization code: {str(e)}")

    async def refresh_token(self) -> TokenInfo:
        """
        Refresh the access token using the refresh token asynchronously.
        """
        if not self._token_info or not self._token_info.refresh_token:
            raise BasalamAuthError("No refresh token available")

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self._token_info.refresh_token,
            }

            try:
                response = await client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()

                # Create a new token info
                previous_refresh_token = self._token_info.refresh_token
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    # Some servers might not include the refresh token in the response
                    # In that case, keep using the previous refresh token
                    refresh_token=token_data.get("refresh_token", previous_refresh_token),
                    scope=token_data.get("scope", self._token_info.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to refresh token: {str(e)}")

    def refresh_token_sync(self) -> TokenInfo:
        """
        Refresh the access token using the refresh token synchronously.
        """
        if not self._token_info or not self._token_info.refresh_token:
            raise BasalamAuthError("No refresh token available")

        with httpx.Client(timeout=self.config.timeout) as client:
            data = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self._token_info.refresh_token,
            }

            try:
                response = client.post(self.config.token_url, data=data)
                response.raise_for_status()

                # Parse and store the token data
                token_data = response.json()

                # Create a new token info
                previous_refresh_token = self._token_info.refresh_token
                self._token_info = TokenInfo(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in", 3600),
                    # Some servers might not include the refresh token in the response
                    # In that case, keep using the previous refresh token
                    refresh_token=token_data.get("refresh_token", previous_refresh_token),
                    scope=token_data.get("scope", self._token_info.scope),
                )

                return self._token_info
            except httpx.HTTPError as e:
                raise BasalamAuthError(f"Failed to refresh token: {str(e)}")

    async def get_token(self) -> TokenInfo:
        """
        Get a token asynchronously (uses refresh if available).
        """
        if not self._token_info:
            raise BasalamAuthError("No token available. You must first exchange an authorization code.")

        if self._token_info.should_refresh and self._token_info.refresh_token:
            return await self.refresh_token()

        return self._token_info

    def get_token_sync(self) -> TokenInfo:
        """
        Get a token synchronously.
        """
        if not self._token_info:
            raise BasalamAuthError("No token available. You must first exchange an authorization code.")

        if self._token_info.should_refresh and self._token_info.refresh_token:
            return self.refresh_token_sync()

        return self._token_info
