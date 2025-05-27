"""
Base client for making requests to the Basalam API.
"""
import asyncio
import json
from functools import wraps
from typing import Any, Dict, List, Optional, Union, TypeVar, Type
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from .auth import BaseAuth
from .config import BasalamConfig
from .errors import BasalamError, BasalamAPIError, BasalamAuthError

# Type variable for response models
T = TypeVar('T', bound=BaseModel)


def refresh_token_on_auth_error(func):
    """
    Decorator to handle token refresh on authentication error.
    Will attempt to refresh the token and retry the request once if
    authentication fails with a 401 error.
    """

    @wraps(func)
    async def async_wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except BasalamAuthError:
            # Try to refresh the token and retry once
            await self.auth.refresh_token()
            return await func(self, *args, **kwargs)

    @wraps(func)
    def sync_wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except BasalamAuthError:
            # Try to refresh the token and retry once
            self.auth.refresh_token_sync()
            return func(self, *args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


class BaseClient:
    """
    Base client for making requests to the Basalam API.

    This class handles HTTP requests, authentication, and error handling.
    It serves as the foundation for all service-specific clients.
    """

    def __init__(
            self,
            auth: BaseAuth,
            config: Optional[BasalamConfig] = None,
            service: Optional[str] = None,
    ):
        """
        Initialize the base client.
        """
        self.auth = auth
        self.config = config or BasalamConfig()
        self.service = service

        # Set the base URL for this service
        if service:
            self.base_url = self.config.get_service_url(service)
        else:
            self.base_url = self.config.base_url

    async def _get_client(self) -> httpx.AsyncClient:
        """Get an async HTTP client with proper configuration."""
        headers = self.config.get_headers()
        auth_headers = await self.auth.get_auth_headers()
        headers.update(auth_headers)

        return httpx.AsyncClient(
            headers=headers,
            timeout=self.config.timeout,
            follow_redirects=True,
        )

    def _get_client_sync(self) -> httpx.Client:
        """Get a synchronous HTTP client with proper configuration."""
        headers = self.config.get_headers()
        auth_headers = self.auth.get_auth_headers_sync()
        headers.update(auth_headers)

        return httpx.Client(
            headers=headers,
            timeout=self.config.timeout,
            follow_redirects=True,
        )

    @staticmethod
    def _handle_http_error(e: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors and convert them to Basalam exceptions."""
        if e.response.status_code == 401:
            raise BasalamAuthError(f"Authentication failed: {e}", response=e.response)

        try:
            error_data = e.response.json()
            error_message = error_data.get("message", str(e))
            error_code = error_data.get("code", e.response.status_code)
        except (json.JSONDecodeError, ValueError):
            error_message = str(e)
            error_code = e.response.status_code

        raise BasalamAPIError(
            message=error_message,
            status_code=e.response.status_code,
            code=error_code,
            response=e.response,
        )

    @staticmethod
    def _parse_response_data(
            response: httpx.Response,
            response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Parse response data and validate with model if provided."""
        # Handle empty responses
        if not response.content:
            return {}

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise BasalamError(f"Invalid JSON response: {response.text}")

        # Parse the response using the provided model
        if response_model:
            if isinstance(data, list):
                return [response_model.model_validate(item) for item in data]
            return response_model.model_validate(data)

        return data

    @refresh_token_on_auth_error
    async def request(
            self,
            method: str,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """
        Make an async request to the API.
        """
        url = urljoin(self.base_url, path)

        async with await self._get_client() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=headers,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                self._handle_http_error(e)

            except httpx.RequestError as e:
                raise BasalamError(f"Request failed: {e}")

            return self._parse_response_data(response, response_model)

    @refresh_token_on_auth_error
    def request_sync(
            self,
            method: str,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """
        Make a synchronous request to the API.
        """
        url = urljoin(self.base_url, path)

        with self._get_client_sync() as client:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=headers,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                self._handle_http_error(e)

            except httpx.RequestError as e:
                raise BasalamError(f"Request failed: {e}")

            return self._parse_response_data(response, response_model)

    async def get(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a GET request."""
        return await self.request("GET", path, params=params, headers=headers, response_model=response_model)

    def get_sync(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous GET request."""
        return self.request_sync("GET", path, params=params, headers=headers, response_model=response_model)

    async def post(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a POST request."""
        return await self.request("POST", path, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model)

    def post_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous POST request."""
        return self.request_sync("POST", path, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model)

    async def put(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a PUT request."""
        return await self.request("PUT", path, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model)

    def put_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous PUT request."""
        return self.request_sync("PUT", path, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model)

    async def patch(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a PATCH request."""
        return await self.request("PATCH", path, data=data, json_data=json_data, headers=headers,
                                  response_model=response_model)

    def patch_sync(
            self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous PATCH request."""
        return self.request_sync("PATCH", path, data=data, json_data=json_data, headers=headers,
                                 response_model=response_model)

    async def delete(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a DELETE request."""
        return await self.request("DELETE", path, params=params, headers=headers, response_model=response_model)

    def delete_sync(
            self,
            path: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            response_model: Optional[Type[T]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], T]:
        """Make a synchronous DELETE request."""
        return self.request_sync("DELETE", path, params=params, headers=headers, response_model=response_model)
