"""
Integration tests for the authentication module using real API calls.
"""
import pytest

from basalam_sdk.auth import (
    TokenInfo, ClientCredentials, AuthorizationCode
)
from basalam_sdk.config import BasalamConfig, Environment
from basalam_sdk.errors import BasalamAuthError

# Real test client credentials
TEST_CLIENT_ID = ""
TEST_CLIENT_SECRET = ""
TEST_REDIRECT_URI = ""


@pytest.fixture
def integration_config():
    """Create a real config for integration testing."""
    return BasalamConfig(
        environment=Environment.PRODUCTION,
        timeout=30.0,
        user_agent="SDK-Test"
    )


@pytest.fixture
def client_credentials_auth(integration_config):
    """Create a real ClientCredentials auth instance for integration testing."""
    return ClientCredentials(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        scopes=["vendor.profile.read", "vendor.profile.write"],
        config=integration_config
    )


@pytest.fixture
def authorization_code_auth(integration_config):
    """Create a real AuthorizationCode auth instance for integration testing."""
    return AuthorizationCode(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        redirect_uri=TEST_REDIRECT_URI,
        scopes=["vendor.profile.read", "vendor.profile.write"],
        config=integration_config
    )


@pytest.mark.integration
class TestClientCredentialsIntegration:
    """Integration tests for ClientCredentials authentication with real API calls."""

    def test_get_token_sync_success(self, client_credentials_auth):
        """Test successful synchronous token acquisition with real API call."""
        token = client_credentials_auth.get_token_sync()

        # Verify token structure
        assert isinstance(token, TokenInfo)
        assert token.access_token is not None
        assert len(token.access_token) > 10  # Should be a substantial token
        assert token.token_type == "Bearer"
        assert token.expires_in > 0
        assert token.created_at is not None

        # Verify token timing
        assert not token.is_expired
        assert not token.should_refresh  # Fresh token shouldn't need refresh

        # Verify scopes (if returned by the API)
        if token.scope:
            granted_scopes = token.granted_scopes
            assert len(granted_scopes) > 0
            # Check if at least one expected scope is granted
            expected_scopes = {"vendor.profile.read", "vendor.profile.write"}
            assert len(granted_scopes.intersection(expected_scopes)) > 0

        # Verify the auth instance stores the token
        assert client_credentials_auth._token_info == token

    @pytest.mark.asyncio
    async def test_get_token_async_success(self, client_credentials_auth):
        """Test successful asynchronous token acquisition with real API call."""
        # Clear any existing token
        client_credentials_auth._token_info = None

        token = await client_credentials_auth.get_token()

        # Verify token structure
        assert isinstance(token, TokenInfo)
        assert token.access_token is not None
        assert len(token.access_token) > 10
        assert token.token_type == "Bearer"
        assert token.expires_in > 0

        # Verify token is valid and fresh
        assert not token.is_expired
        assert not token.should_refresh

    def test_get_auth_headers_sync(self, client_credentials_auth):
        """Test getting auth headers with a real token."""
        # Get a real token first
        token = client_credentials_auth.get_token_sync()

        # Get auth headers
        headers = client_credentials_auth.get_auth_headers_sync()

        assert "Authorization" in headers
        expected_header = f"{token.token_type} {token.access_token}"
        assert headers["Authorization"] == expected_header

    @pytest.mark.asyncio
    async def test_get_auth_headers_async(self, client_credentials_auth):
        """Test getting auth headers asynchronously with a real token."""
        # Clear any existing token
        client_credentials_auth._token_info = None

        # Get auth headers (should fetch token automatically)
        headers = await client_credentials_auth.get_auth_headers()

        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Bearer ")

        # Verify token was stored
        assert client_credentials_auth._token_info is not None

    def test_refresh_token_sync_success(self, client_credentials_auth):
        """Test successful synchronous token refresh."""
        # Get initial token
        initial_token = client_credentials_auth.get_token_sync()
        initial_access_token = initial_token.access_token

        # Refresh token (for client credentials, this gets a new token)
        refreshed_token = client_credentials_auth.refresh_token_sync()

        # Verify we got a token back
        assert isinstance(refreshed_token, TokenInfo)
        assert refreshed_token.access_token is not None

        # For client credentials flow, refresh might return the same token
        # if it's still valid, or a new one
        assert refreshed_token.token_type == "Bearer"
        assert refreshed_token.expires_in > 0

    @pytest.mark.asyncio
    async def test_refresh_token_async_success(self, client_credentials_auth):
        """Test successful asynchronous token refresh."""
        # Get initial token
        initial_token = await client_credentials_auth.get_token()

        # Refresh token
        refreshed_token = await client_credentials_auth.refresh_token()

        # Verify we got a token back
        assert isinstance(refreshed_token, TokenInfo)
        assert refreshed_token.access_token is not None
        assert refreshed_token.token_type == "Bearer"

    def test_scope_validation(self, client_credentials_auth):
        """Test scope validation with a real token."""
        # Get a real token
        token = client_credentials_auth.get_token_sync()

        # Test scope checking
        if token.scope:
            granted_scopes = client_credentials_auth.get_granted_scopes()
            assert isinstance(granted_scopes, set)
            assert len(granted_scopes) > 0

            # Test has_scope method
            for scope in granted_scopes:
                assert client_credentials_auth.has_scope(scope)

            # Test with a scope we definitely don't have
            assert not client_credentials_auth.has_scope("non.existent.scope")

    def test_multiple_scopes_request(self, integration_config):
        """Test requesting multiple scopes."""
        auth = ClientCredentials(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET,
            scopes=["vendor.profile.read", "vendor.profile.write", "vendor.product.read"],
            config=integration_config
        )

        token = auth.get_token_sync()

        assert isinstance(token, TokenInfo)
        assert token.access_token is not None

        # Check if multiple scopes were granted (if the API supports it)
        if token.scope:
            granted_scopes = token.granted_scopes
            # We should have at least one of our requested scopes
            requested_scopes = {"vendor.profile.read", "vendor.profile.write", "vendor.product.read"}
            assert len(granted_scopes.intersection(requested_scopes)) > 0


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Integration tests for error handling with real API calls."""

    def test_invalid_client_credentials(self, integration_config):
        """Test behavior with invalid client credentials."""
        auth = ClientCredentials(
            client_id="invalid_client_id",
            client_secret="invalid_client_secret",
            scopes=["vendor.profile.read"],
            config=integration_config
        )

        # Should raise an authentication error
        with pytest.raises(BasalamAuthError) as exc_info:
            auth.get_token_sync()

        assert "Failed to get access token" in str(exc_info.value)

    def test_invalid_scope_request(self, integration_config):
        """Test behavior when requesting invalid scopes."""
        auth = ClientCredentials(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET,
            scopes=["completely.invalid.scope.that.does.not.exist"],
            config=integration_config
        )

        try:
            token = auth.get_token_sync()
            if token.scope:
                assert "completely.invalid.scope.that.does.not.exist" not in token.granted_scopes
        except BasalamAuthError:
            pass

    @pytest.mark.asyncio
    async def test_network_timeout_handling(self, integration_config):
        """Test behavior with very short timeout."""
        short_timeout_config = BasalamConfig(
            environment=Environment.PRODUCTION,
            timeout=0.001  # 1ms - should timeout
        )

        auth = ClientCredentials(
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET,
            config=short_timeout_config
        )

        with pytest.raises(BasalamAuthError):
            await auth.get_token()
