"""
This module defines the Pydantic schemas used for validating and serializing requests and responses
related to QR code generation.
"""

from typing import List, Optional

from pydantic import BaseModel, HttpUrl, Field, conint

class QRCodeRequest(BaseModel):
    """
    Schema for a QR code request.
    It includes the URL to be encoded, color settings, and size.
    """
    url: HttpUrl = Field(..., description="The URL to encode into the QR code.")
    fill_color: str = Field(
        default="red",
        description="Color of the QR code.",
        example="black"
    )
    back_color: str = Field(
        default="white",
        description="Background color of the QR code.",
        example="yellow"
    )
    size: conint(ge=1, le=40) = Field(
        default=10,
        description="Size of the QR code from 1 to 40.",
        example=20
    )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Additional configuration for the QRCodeRequest schema.
        """
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "fill_color": "black",
                "back_color": "yellow",
                "size": 20
            }
        }


class Link(BaseModel):
    """
    Schema for a hyperlink with details for the relation type, URL, and HTTP method.
    """
    rel: str
    href: HttpUrl
    action: str
    type: str

    class Config:  # pylint: disable=too-few-public-methods
        """
        Additional configuration for the Link schema.
        Includes examples for JSON serialization.
        """
        json_schema_extra = {
            "example": {
                "rel": "self",
                "href": "https://api.example.com/qr/123",
                "action": "GET",
                "type": "application/json"
            }
        }


class QRCodeResponse(BaseModel):
    """
    Schema for the response returned after generating a QR code.
    Includes a message, the URL of the generated QR code, and related links.
    """
    message: str
    qr_code_url: HttpUrl
    links: List[Link] = []

    class Config:  # pylint: disable=too-few-public-methods
        """
        Additional configuration for the Link schema.
        Includes examples for JSON serialization.
        """
        json_schema_extra = {
            "example": {
                "message": "QR code created successfully.",
                "qr_code_url": "https://api.example.com/qr/123",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/qr/123",
                        "action": "GET",
                        "type": "application/json"
                    }
                ]
            }
        }


class Token(BaseModel):
    """
    Schema for the authentication token response.
    """
    access_token: str = Field(
        ...,
        description="The access token for authentication."
    )
    token_type: str = Field(
        default="bearer",
        description="The type of the token."
    )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Additional configuration for the Link schema.
        Includes examples for JSON serialization.
        """
        json_schema_extra = {
            "example": {
                "access_token": "jhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """
    Schema for the data within a token, typically used to identify a user.
    """
    username: Optional[str] = Field(
        None,
        description="The username that the token represents."
    )

    class Config:  # pylint: disable=too-few-public-methods
        """
        Additional configuration for the Link schema.
        Includes examples for JSON serialization.
        """
        json_schema_extra = {
            "example": {
                "username": "user@example.com"
            }
        }
