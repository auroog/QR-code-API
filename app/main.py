"""
Main module for the FastAPI QR Code Manager application. This file initializes
the FastAPI app, sets up the logging configuration, and includes routes for
managing QR codes and handling OAuth authentication.
"""

from fastapi import FastAPI
from app.config import QR_DIRECTORY
from app.routers import qr_code, oauth
from app.services.qr_service import create_directory
from app.utils.common import setup_logging
from app.schema import QRCodeRequest, QRCodeResponse, Link
from pydantic import HttpUrl

setup_logging()

create_directory(QR_DIRECTORY)

app = FastAPI(
    title="QR Code Manager",
    description=(
        "A FastAPI application for creating, listing available codes, and deleting QR codes."
        "It also supports OAuth for secure access."
    ),
    version="0.0.1",
    redoc_url=None,
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.include_router(qr_code.router)
app.include_router(oauth.router)

@app.get("/")
async def read_root():
    """
    Root endpoint that displays a welcome message.
    """
    return {"message": "Welcome to the QR Code Manager API"}

@app.post("/generate_qr", response_model=QRCodeResponse)
async def generate_qr_code(request: QRCodeRequest):
    """
    Generate a QR code based on the request parameters and return the URL
    and related links in the QRCodeResponse format.
    """

    qr_code_url = f"https://example.com/qr/{request.url}"

    links = [
        Link(
            rel="self",
            href=f"https://api.example.com/qr/{request.url}",
            action="GET"
        ),
        Link(
            rel="delete",
            href=f"https://api.example.com/qr/{request.url}",
            action="DELETE"
        )
    ]

    return QRCodeResponse(
        message="QR code created successfully.",
        qr_code_url=HttpUrl(qr_code_url),
        links=links
    )
