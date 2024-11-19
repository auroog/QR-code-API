"""
This module contains pytest fixtures for the test suite.
"""

import pytest
from httpx import AsyncClient
from app.main import app  # Adjust import path as necessary

@pytest.fixture
async def client():
    """
    Creates an asynchronous HTTP client for testing FastAPI routes.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
async def get_access_token_for_test(client):  # pylint: disable=redefined-outer-name
    """
    Retrieves an access token for testing by posting valid credentials to the token endpoint.

    Args:
        client: The HTTP client fixture.

    Returns:
        A valid access token as a string.
    """
    form_data = {"username": "admin", "password": "secret"}
    response = await client.post("/token", data=form_data)
    return response.json()["access_token"]
