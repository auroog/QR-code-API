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
    Message will display
    """
    return {"message":"Welcome to the QR Code Manager API"}
