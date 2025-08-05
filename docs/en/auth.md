# Authentication Guide

The SDK supports three main authentication methods, all managed via authentication objects implementing the `BaseAuth`
interface:

- **Personal Access Token** – for personal or dedicated applications
- **Authorization Code Flow** – for user authentication scenarios on third-party platforms
- **Client Credentials** – for applications with legal/organizational access

For more information about these methods, refer to the [Authentication in Basalam API](../../quick-start#auth) document.

## Table of Contents

- [Personal Access Token](#personal-access-token)
- [Authorization Code Flow](#authorization-code-flow-for-user-authentication)
- [Client Credentials](#client-credentials)
- [Token Management](#token-management)
- [Scopes](#scopes)

## Personal Access Token

For personal applications for a booth or user,
after [getting your token from the developer panel](https://developers.basalam.com/panel/tokens), you can manage it
using `PersonalToken`.

```python
from basalam_sdk import BasalamClient, PersonalToken


def personal_token_example():
    # Initialize with existing tokens
    auth = PersonalToken(
        token="your_access_token",
        refresh_token="your_refresh_token",
    )

    # Create an authenticated client
    client = BasalamClient(auth=auth)

    # Get current user info
    user = client.get_current_user()
    return user
```

## Authorization Code Flow (for user authentication)

When building a third-party app requiring access from users,
after [creating a client in the developer panel](https://developers.basalam.com/panel/clients), use the
`AuthorizationCode` class to manage the flow.

```python
from basalam_sdk import BasalamClient, AuthorizationCode, Scope

# Step 1: Create the auth object
auth = AuthorizationCode(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
    scopes=[
        Scope.CUSTOMER_WALLET_READ,
        Scope.CUSTOMER_ORDER_READ
    ]
)

# Step 2: Get authorization URL
auth_url = auth.get_authorization_url(state="optional_state_parameter")
print(f"Visit: {auth_url}")

# Step 3: Exchange code for tokens (after receiving the code from the registered redirect URI)
token_info = auth.get_token(code="authorization_code_from_callback")

# Step 4: Create an authenticated client
client = BasalamClient(auth=auth)
```

### Usage Example

```python
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/login')
def login():
    auth = AuthorizationCode(
        client_id="your-client-id",
        client_secret="your-client-secret",
        redirect_uri="https://your-app.com/callback"
    )

    auth_url = auth.get_authorization_url(state="user_session_id")
    return redirect(auth_url)

@app.route('/callback')
async def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    auth = AuthorizationCode(
        client_id="your-client-id",
        client_secret="your-client-secret",
        redirect_uri="https://your-app.com/callback"
    )

    # Exchange code for tokens
    token_info = await auth.get_token(code=code)

    # Securely store tokens
    # ... save token_info.access_token, token_info.refresh_token

    return "Authentication successful!"
```

## Client Credentials

To use APIs requiring organizational identity (e.g., Wallet),
after [client authentication](../../quick-start#client_credentials) using `grant_type="client_credentials"`, use
`ClientCredentials`.

### Initial Configuration

```python
from basalam_sdk import BasalamClient, ClientCredentials

# Basic authentication
auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=[
        Scope.CUSTOMER_WALLET_READ,
        Scope.VENDOR_PRODUCT_WRITE
    ]
)

# Create client
client = BasalamClient(auth=auth)
```

### Usage Example

```python
from basalam_sdk import BasalamClient, ClientCredentials


async def client_credentials_example():
    auth = ClientCredentials(
        client_id="your-client-id",
        client_secret="your-client-secret"
    )
    client = BasalamClient(auth=auth)

    # Get user balance
    balance = await client.get_balance(user_id=123)

    return balance
```

## Token Management

### Get Token Info

```python
from basalam_sdk import BasalamClient, ClientCredentials

async def token_management_example():
    auth = ClientCredentials(
        client_id="your-client-id",
        client_secret="your-client-secret"
    )

    # Get token – will reuse existing one if not expired
    token_info = await auth.get_token()

    return token_info
```

## Scopes

Scopes define the permissions granted to your app. In addition to
the [Scopes doc](https://developers.basalam.com/scopes), the SDK provides scopes via the `Scope` class. Available scopes
include:

```python
from basalam_sdk import Scope

# Common scopes
Scope.CUSTOMER_WALLET_READ      # Read customer wallet
Scope.CUSTOMER_WALLET_WRITE     # Write to customer wallet
Scope.VENDOR_PRODUCT_READ       # Read vendor products
Scope.VENDOR_PRODUCT_WRITE      # Write vendor products
Scope.CUSTOMER_ORDER_READ       # Read customer orders
Scope.CUSTOMER_ORDER_WRITE      # Write customer orders
```

### Using Scopes

```python
from basalam_sdk import ClientCredentials, Scope

auth = ClientCredentials(
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=[
        Scope.CUSTOMER_WALLET_READ,
        Scope.VENDOR_PRODUCT_WRITE,
        Scope.CUSTOMER_ORDER_READ
    ]
)
```
