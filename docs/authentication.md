# Authentication Guide

This document provides detailed information about authentication mechanisms in the Basalam SDK, including the various
authentication methods, token management, and security considerations.

## Table of Contents

1. [Authentication Overview](#authentication-overview)
2. [Authentication Methods](#authentication-methods)
    - [Client Credentials](#client-credentials)
    - [Authorization Code](#authorization-code)
3. [Token Management](#token-management)
4. [Security Best Practices](#security-best-practices)
5. [Troubleshooting](#troubleshooting)

## Authentication Overview

The Basalam SDK supports OAuth 2.0 for authentication, providing secure access to Basalam APIs. OAuth 2.0 allows
applications to obtain limited access to user accounts or obtain application-level access without user involvement.

### Authentication Components

The authentication system consists of several components:

1. **Auth Base Class**: The core `BaseAuth` class in `auth.py`
2. **Auth Implementations**: Concrete implementations for different authentication methods
3. **Token Management**: Handling token storage, refreshing, and validation
4. **Client Integration**: How authentication integrates with API clients

## Authentication Methods

### Client Credentials

The Client Credentials method is used for server-to-server authentication when no user context is required. This method
is suitable for accessing APIs that are not user-specific.

#### Implementation

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import ClientCredentials

# Create an authentication object
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=["webhook:read", "wallet:read"]  # Request specific scopes
)

# Create client with the authentication object
client = BasalamClient(auth=auth)

# Use the authenticated client
webhooks = client.webhook.get_webhooks_sync()
```

#### When to Use

- Backend services that need to access Basalam APIs
- Batch processes or scripts
- Systems where no user interaction is required or available
- Administrative tasks that require elevated privileges

### Authorization Code

The Authorization Code method is used to obtain access tokens on behalf of a user. This method involves redirecting the
user to the Basalam authorization server, where they authenticate and consent to the requested permissions.

#### Implementation

```python
from basalam_sdk import BasalamClient
from basalam_sdk.auth import AuthorizationCode

# Create an authorization object
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=["webhook:read", "wallet:read", "profile:read"]
)

# Step 1: Generate the authorization URL
auth_url = auth.get_authorization_url(state="random-state-value")
# Redirect user to auth_url in your web application

# Step 2: In your callback handler, exchange code for token
def callback_handler(code):
    # Exchange the authorization code for a token
    token_info = auth.exchange_code_sync(code)
    
    # Create a client with the auth object
    client = BasalamClient(auth=auth)
    return client
```

#### Web Application Example

Here's a simplified web application example using Flask:

```python
from flask import Flask, request, redirect, session
from basalam_sdk import BasalamClient
from basalam_sdk.auth import AuthorizationCode
import secrets

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Configure auth object
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:5000/callback",
    scopes=["profile:read", "webhook:read"]
)

@app.route("/login")
def login():
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state
    
    # Generate authorization URL
    auth_url = auth.get_authorization_url(state=state)
    
    # Redirect user to authorization server
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Verify state to prevent CSRF
    if request.args.get("state") != session.get("oauth_state"):
        return "State mismatch. Possible CSRF attack.", 400
    
    # Exchange code for token
    code = request.args.get("code")
    if not code:
        return "No authorization code provided.", 400
    
    try:
        # Exchange code for token
        token_info = auth.exchange_code_sync(code)
        
        # Store auth in session (for demonstration only)
        session["authenticated"] = True
        
        return redirect("/profile")
    except Exception as e:
        return f"Error: {str(e)}", 400

@app.route("/profile")
def profile():
    if not session.get("authenticated"):
        return redirect("/login")
    
    # Create client with the auth object
    client = BasalamClient(auth=auth)
    
    # Use client to get profile data
    # ...
    
    return "Profile data would be displayed here."
```

#### When to Use

- Web applications that need to access user-specific data
- Mobile applications that integrate with Basalam
- Any scenario where user consent is required for API access
- Applications that need to perform actions on behalf of a user

## Token Management

The SDK handles token management internally through the authentication objects.

### Token Structure

Token information is represented by the `TokenInfo` class with the following structure:

```python
@dataclass
class TokenInfo:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: float = None
```

### Automatic Token Refresh

The SDK automatically refreshes tokens when they expire:

```python
# Create the authentication object
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Create client with the auth object
client = BasalamClient(auth=auth)

# The token will be automatically obtained when making the first API call
# and refreshed when it expires

# You can also manually refresh the token
client.refresh_auth_token_sync()  # Synchronous refresh
await client.refresh_auth_token()  # Asynchronous refresh
```

### Checking Token State

You can check the current token state:

```python
# Get the token info
token_info = auth.token_info

# Check if token exists and is valid
if token_info and not token_info.is_expired:
    print(f"Token valid for {token_info.expires_at - time.time()} more seconds")

# Check if token should be refreshed soon
if token_info and token_info.should_refresh:
    print("Token should be refreshed soon")
```

## Security Best Practices

When implementing authentication with the Basalam SDK, follow these security best practices:

### Protecting Client Secrets

- Never commit client secrets to source control
- Use environment variables or secure vaults for secrets
- Restrict access to client secrets to only those who need it

```python
import os
from basalam_sdk.auth import ClientCredentials
from basalam_sdk import BasalamClient

# Load client secret from environment variable
client_id = os.environ.get("BASALAM_CLIENT_ID")
client_secret = os.environ.get("BASALAM_CLIENT_SECRET")

auth = ClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

client = BasalamClient(auth=auth)
```

### Secure Token Storage

- Encrypt tokens before storing them
- Use secure, platform-appropriate storage mechanisms
- Implement token rotation policies

### Scope Management

- Request only the scopes your application needs
- Document the required scopes in your application
- Verify scopes in received tokens match expected scopes

```python
# Request minimal scopes
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=["webhook:read"]  # Only request what's needed
)

# Verify scopes after authentication
if auth.has_scope("webhook:read"):
    # Proceed with webhook operations
    pass
else:
    print("Missing required scope: webhook:read")
```

### CSRF Protection

- Always use the state parameter in authorization flows
- Verify the state parameter in callbacks
- Use cryptographically secure random values for state

### Handling Token Expiry

- Token expiry is handled automatically by the SDK
- You can manually check if a token is expired with `token_info.is_expired`
- You can manually refresh a token with `client.refresh_auth_token_sync()`

## Troubleshooting

### Common Authentication Issues

#### Invalid Client Error

```
{
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
```

**Possible Causes:**

- Incorrect client ID or client secret
- Client ID is not authorized for the requested grant type
- Client credentials sent in the wrong format

**Solution:**

- Verify client ID and secret are correct
- Ensure the client is configured for the grant type you're using
- Check if credentials should be sent in Authorization header or request body

#### Invalid Grant Error

```
{
  "error": "invalid_grant",
  "error_description": "Invalid authorization code"
}
```

**Possible Causes:**

- Authorization code has expired (they typically expire quickly)
- Code has already been used
- Redirect URI doesn't match the one used in the authorization request

**Solution:**

- Ensure you're exchanging the code promptly after receiving it
- Never reuse authorization codes
- Use the exact same redirect URI throughout the flow

#### Token Expired Error

```
{
  "error": "invalid_token",
  "error_description": "The access token expired"
}
```

**Possible Causes:**

- Access token has expired
- Token expiry time calculation is incorrect

**Solution:**

- The SDK will automatically refresh tokens when they expire
- You can manually refresh a token with `client.refresh_auth_token_sync()`
- Verify server and client clock synchronization

### Debugging Authentication

The SDK provides built-in logging that can help diagnose authentication issues:

```python
import logging

# Enable DEBUG level logging
logging.basicConfig(level=logging.DEBUG)

# Create the auth object and client
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret"
)
client = BasalamClient(auth=auth)
```

### Error Reference

| Error Code               | Description                                      | Possible Cause                              | Solution                                                                               |
|--------------------------|--------------------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------|
| `invalid_request`        | The request is missing a required parameter      | Missing parameter in authentication request | Check request parameters against OAuth 2.0 specifications                              |
| `invalid_client`         | Client authentication failed                     | Incorrect client credentials                | Verify client ID and secret                                                            |
| `invalid_grant`          | The provided authorization grant is invalid      | Expired or invalid code/token               | Request a new authorization code                                                       |
| `unauthorized_client`    | The client is not authorized for this grant type | Client not configured for grant type        | Check client configuration in Basalam developer portal                                 |
| `unsupported_grant_type` | The grant type is not supported                  | Using an unsupported grant type             | Use only supported grant types (client_credentials, authorization_code, refresh_token) |
| `invalid_scope`          | The requested scope is invalid or unknown        | Requesting unauthorized scopes              | Check available scopes for your client                                                 |
| `access_denied`          | The resource owner denied the request            | User rejected the authorization             | Explain to users why permissions are needed                                            |
| `server_error`           | Server error                                     | Internal server error                       | Retry with exponential backoff                                                         |

By following this guide, you should be able to implement secure and reliable authentication with the Basalam SDK for
your application's specific needs. 
