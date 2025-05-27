#!/usr/bin/env python
"""
Authorization Code Authentication Example

This example demonstrates how to use the Authorization Code authentication
method with the Basalam SDK. It shows a simplified Flask web app that
handles the OAuth 2.0 authorization flow.
"""

import os
import secrets

from flask import Flask, request, redirect, session, render_template_string

from basalam_sdk import BasalamClient
from basalam_sdk.auth import AuthorizationCode

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))

# Get credentials (use environment variables in production)
CLIENT_ID = os.environ.get("BASALAM_CLIENT_ID", "your-client-id")
CLIENT_SECRET = os.environ.get("BASALAM_CLIENT_SECRET", "your-client-secret")
REDIRECT_URI = "http://localhost:5000/callback"

# Create authentication object
auth = AuthorizationCode(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scopes=["profile:read", "webhook:read", "wallet:read"]
)

# Simple HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Basalam SDK Authorization Code Example</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        .button { background-color: #4CAF50; border: none; color: white; padding: 10px 20px; 
                 text-align: center; text-decoration: none; display: inline-block; 
                 font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Basalam SDK Authorization Code Example</h1>
    
    <div class="card">
        <h2>Authentication Status</h2>
        {% if authenticated %}
            <p>✅ You are authenticated!</p>
            <a href="/profile" class="button">View Profile</a>
            <a href="/webhooks" class="button">List Webhooks</a>
            <a href="/wallet" class="button">Check Wallet</a>
            <a href="/logout" class="button" style="background-color: #f44336;">Logout</a>
        {% else %}
            <p>❌ You are not authenticated.</p>
            <a href="/login" class="button">Login with Basalam</a>
        {% endif %}
    </div>
</body>
</html>
"""

# Simple template for displaying API data
DATA_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - Basalam SDK Example</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        .button { background-color: #2196F3; border: none; color: white; padding: 10px 20px; 
                 text-align: center; text-decoration: none; display: inline-block; 
                 font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px; }
        pre { background-color: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    
    <div class="card">
        <pre>{{ data }}</pre>
        <a href="/" class="button">Back to Home</a>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    """Home page."""
    # Check if user is authenticated
    authenticated = session.get("authenticated", False)
    return render_template_string(HOME_TEMPLATE, authenticated=authenticated)


@app.route("/login")
def login():
    """Initiate the authorization flow."""
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state

    # Generate authorization URL with state
    auth_url = auth.get_authorization_url(state=state)

    # Redirect to authorization server
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """Handle the OAuth callback."""
    # Verify state parameter to prevent CSRF attacks
    if request.args.get("state") != session.get("oauth_state"):
        return "State mismatch. Possible CSRF attack.", 400

    # Get the authorization code
    code = request.args.get("code")
    if not code:
        return "No authorization code provided.", 400

    try:
        # Exchange the code for a token
        token_info = auth.exchange_code_sync(code)

        # Mark the session as authenticated
        session["authenticated"] = True

        return redirect("/")
    except Exception as e:
        return f"Error exchanging code for token: {str(e)}", 400


@app.route("/profile")
def profile():
    """Display user profile information."""
    if not session.get("authenticated"):
        return redirect("/login")

    try:
        # Create the client with our auth object
        client = BasalamClient(auth=auth)

        # Get user profile data
        # This is a placeholder - implement based on your API
        profile_data = "User profile data would be displayed here."

        return render_template_string(
            DATA_TEMPLATE,
            title="User Profile",
            data=profile_data
        )
    except Exception as e:
        return f"Error: {str(e)}", 400


@app.route("/webhooks")
def webhooks():
    """Display webhooks information."""
    if not session.get("authenticated"):
        return redirect("/login")

    try:
        # Create the client with our auth object
        client = BasalamClient(auth=auth)

        # Get webhooks
        webhooks = client.webhook.get_webhooks_sync()

        # Format data for display
        webhook_data = f"Found {webhooks.result_count} webhooks"

        return render_template_string(
            DATA_TEMPLATE,
            title="Webhooks",
            data=webhook_data
        )
    except Exception as e:
        return f"Error: {str(e)}", 400


@app.route("/wallet")
def wallet():
    """Display wallet information."""
    if not session.get("authenticated"):
        return redirect("/login")

    try:
        # Create the client with our auth object
        client = BasalamClient(auth=auth)

        # Get wallet balance
        balance = client.wallet.get_balance_sync()

        # Format data for display
        wallet_data = f"Balance: {balance.amount} {balance.currency}"

        return render_template_string(
            DATA_TEMPLATE,
            title="Wallet",
            data=wallet_data
        )
    except Exception as e:
        return f"Error: {str(e)}", 400


@app.route("/logout")
def logout():
    """Log the user out."""
    # Clear the session
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    print("=== Basalam SDK Authorization Code Example ===")
    print(f"Server running at http://localhost:5000")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Redirect URI: {REDIRECT_URI}")

    app.run(debug=True, host="localhost", port=5000)
