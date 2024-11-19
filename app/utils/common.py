"""
Module for URL validation, JWT generation, password verification, and URL expiration handling.

This module provides functions to:
- Validate and parse URLs.
- Generate and validate JWT tokens.
- Verify passwords.
- Check if a URL has expired based on timestamp.
- Encode/decode filename for URL-safe usage.
- Generate links based on a URL pattern.
"""

import logging
from urllib.parse import urlparse,parse_qs
from datetime import datetime, timedelta
from jose import jwt, JWTError
import validators
from app.config import ALGORITHM, SECRET_KEY

def setup_logging():
    """
    Set up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def authenticate_user(username: str, password: str):
    """
    Authenticate a user based on the provided credentials.
    Replace this function with a real user validation against a database.

    Args:
        username (str): The username.
        password (str): The password.

    Returns:
        dict: A user object or None if authentication fails.
    """
    if username == "admin" and password == "secret":
        return {"username": "admin"}
    return None

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """
    Create a JWT token with the provided data and expiration time.

    Args:
        data (dict): The payload data to encode into the JWT token.
        expires_delta (timedelta): The expiration time of the token (default is 1 hour).

    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_and_parse_url(url: str) -> str:
    """
    Validates and parses the given URL.
    """
    if not validators.url(url):
        raise ValueError("Invalid URL format")
    parsed_url = urlparse(url)
    return parsed_url.geturl()

def generate_jwt_token(payload: dict) -> str:
    """
    Generates a JWT token.
    """
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validate_jwt_token(token: str) -> dict:
    """
    Validates the JWT token.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e

def verify_password(stored_password: str, input_password: str) -> bool:
    """
    Verifies the password.
    """
    return stored_password == input_password

def is_url_expired(url: str, expiration_time: int = 3600) -> bool:
    """
    Checks if the URL has expired based on the given expiration time.
    """
    current_time = datetime.utcnow()
    expiration_delta = timedelta(seconds=expiration_time)
    parsed_url = urlparse(url)
    try:
        timestamp = int(parse_qs(parsed_url.query).get("timestamp", ["0"])[0])
    except ValueError as exc:
        raise ValueError("Invalid timestamp in URL query") from exc

    expiration_datetime = datetime.utcfromtimestamp(timestamp) + expiration_delta
    return current_time > expiration_datetime

def decode_filename_to_url(filename: str) -> str:
    """
    Decodes a filename to a URL-safe format.
    """
    return filename.replace('_', '/').replace('-', '+')

def encode_url_to_filename(url: str) -> str:
    """
    Encodes a URL into a filename-safe format.
    """
    url_str = str(url)
    return url_str.replace('/', '_').replace('+', '-')

def generate_links(filename: str, base_url: str, download_url: str):
    """
    Generates HATEOAS (Hypermedia as the Engine of Application State) links for the given resource.

    Args:
        filename (str): The name of the file for which links are generated.
        base_url (str): The base URL of the server.
        download_url (str): The specific download URL for the file.

    Returns:
        dict: A dictionary containing HATEOAS links.
    """
    return {
        "self": f"{base_url}/qr-codes/{filename}",
        "download": download_url,
        "delete": f"{base_url}/qr-codes/{filename}/delete"
    }
