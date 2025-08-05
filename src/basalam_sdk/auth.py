"""
Authentication module for the Basalam SDK.

This module provides authentication classes for different OAuth2 flows.
It supports both synchronous and asynchronous operations with comprehensive error handling.

Available authentication methods:
- ClientCredentials: For server-to-server API calls
- AuthorizationCode: For user-authorized applications
- PersonalToken: For applications that already have access and refresh tokens

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
    ALL = "*"

    # OrderEnum processing
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


class GrantType(str, Enum):
    """
    Available OAuth grant types for Basalam API.
    """
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"


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
    async def get_token(self, *args, **kwargs) -> TokenInfo:
        """
        Get a token asynchronously.
        """
        pass

    @abstractmethod
    def get_token_sync(self, *args, **kwargs) -> TokenInfo:
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
            scopes: Optional[Union[str, List[Union[str, Scope]]]] = ['*'],
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

    async def get_token(self, *args, **kwargs) -> TokenInfo:
        """
        Get an access token using client credentials flow asynchronously.
        """
        if self._token_info and not self._token_info.should_refresh:
            return self._token_info

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            data = {
                "grant_type": GrantType.CLIENT_CREDENTIALS.value,
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

    def get_token_sync(self, *args, **kwargs) -> TokenInfo:
        """
        Get an access token using client credentials flow synchronously.
        """
        if self._token_info and not self._token_info.should_refresh:
            return self._token_info

        with httpx.Client(timeout=self.config.timeout) as client:
            data = {
                "grant_type": GrantType.CLIENT_CREDENTIALS.value,
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


class PersonalToken(BaseAuth):
    """
    Personal token authentication flow.

    This authentication method is suitable for applications that already have
    access and refresh tokens and want to manage them directly.

    For detailed examples, see: docs/personal_token_example.md
    """

    def __init__(
            self,
            token: str,
            refresh_token: str = "",
            token_type: str = "Bearer",
            expires_in: int = 3600,
            scope: Optional[str] = '*',
            config: Optional[BasalamConfig] = None,
    ):
        """
        Initialize personal token authentication.

        Args:
            token: The access token
            refresh_token: The refresh token
            token_type: The token type (default: "Bearer")
            expires_in: Token expiration time in seconds (default: 3600)
            scope: The granted scopes (default: '*')
            config: Optional configuration
        """
        super().__init__(config)
        self.refresh_token_value = refresh_token

        # Create initial token info
        self._token_info = TokenInfo(
            access_token=token,
            token_type=token_type,
            expires_in=expires_in,
            refresh_token=refresh_token,
            scope=scope,
        )

    async def get_token(self, *args, **kwargs) -> TokenInfo:
        """
        Get the current access token asynchronously.
        """
        return self._token_info

    def get_token_sync(self, *args, **kwargs) -> TokenInfo:
        """
        Get the current access token synchronously.
        """
        return self._token_info

    async def refresh_token(self) -> TokenInfo:
        """
        Refresh the access token asynchronously.

        Note: Personal Token flow doesn't support automatic token refresh.
        You need to provide a new token manually.
        """
        print("Token refresh not supported for PersonalToken authentication. Please provide a new token manually.")
        return self._token_info

    def refresh_token_sync(self) -> TokenInfo:
        """
        Refresh the access token synchronously.

        Note: Personal Token flow doesn't support automatic token refresh.
        You need to provide a new token manually.
        """
        print("Token refresh not supported for PersonalToken authentication. Please provide a new token manually.")
        return self._token_info


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
            scopes: Optional[Union[str, List[Union[str, Scope]]]] = ['*'],
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
            "redirect_uri": self.redirect_uri
        }

        if self.scope:
            params["scope"] = self.scope

        if state:
            params["state"] = state

        # Build the URL
        return f"{self.config.authorize_url}?{urlencode(params)}"

    async def get_token(self, code: Optional[str] = None, *args, **kwargs) -> TokenInfo:
        """
        Get a token asynchronously.
        If token is already available and not expired, returns it.
        If code is provided, exchanges it for a new token.
        """
        # If token is available and not expired, return it
        if self._token_info and not self._token_info.is_expired:
            return self._token_info

        # If no code provided and no token available, raise error
        if not code:
            if not self._token_info:
                raise BasalamAuthError("No token available. You must provide an authorization code.")
            return self._token_info

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            data = {
                "grant_type": GrantType.AUTHORIZATION_CODE.value,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "code": code,
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

    def get_token_sync(self, code: Optional[str] = None, *args, **kwargs) -> TokenInfo:
        """
        Get a token synchronously.
        If token is already available and not expired, returns it.
        If code is provided, exchanges it for a new token.
        """
        # If token is available and not expired, return it
        if self._token_info and not self._token_info.is_expired:
            return self._token_info

        # If no code provided and no token available, raise error
        if not code:
            if not self._token_info:
                raise BasalamAuthError("No token available. You must provide an authorization code.")
            return self._token_info

        with httpx.Client(timeout=self.config.timeout) as client:
            data = {
                "grant_type": GrantType.AUTHORIZATION_CODE.value,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "code": code,
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
        Refresh token functionality is not available in this implementation.
        """
        print("Refresh token functionality is not available for this authorization code implementation.")
        if not self._token_info:
            raise BasalamAuthError("No token available. You must first exchange an authorization code.")
        return self._token_info

    def refresh_token_sync(self) -> TokenInfo:
        """
        Refresh token functionality is not available in this implementation.
        """
        print("Refresh token functionality is not available for this authorization code implementation.")
        if not self._token_info:
            raise BasalamAuthError("No token available. You must first exchange an authorization code.")
        return self._token_info
