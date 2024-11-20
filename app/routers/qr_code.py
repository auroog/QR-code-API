# Disable specific pylint warnings
# pylint: disable=too-many-function-args, unused-argument
"""
This module contains API routes for creating, listing, and deleting QR codes.
It utilizes FastAPI to provide endpoints for generating QR codes,
retrieving existing QR codes, and deleting them, with support for OAuth2 authentication.
"""

# Import necessary modules and functions from FastAPI and other standard libraries
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

# Import classes and functions from our application's modules
from app.schema import QRCodeRequest, QRCodeResponse
from app.services.qr_service import generate_qr_code, list_qr_codes, delete_qr_code
from app.utils.common import decode_filename_to_url, encode_url_to_filename, generate_links
from app.config import QR_DIRECTORY, SERVER_BASE_URL, FILL_COLOR, BACK_COLOR, SERVER_DOWNLOAD_FOLDER
# Create an APIRouter instance to register our endpoints
router = APIRouter()

# Setup OAuth2 with Password (and hashing), using a simple OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define an endpoint to create QR codes
@router.post(
    "/qr-codes/",
    response_model=QRCodeResponse,
    status_code=status.HTTP_200_OK,
    tags=["QR Codes"]
)
async def create_qr_code(request: QRCodeRequest, token: str = Depends(oauth2_scheme)):
    """
    Creates a QR code for the given URL and returns the download URL.
    """
    logging.info("Creating QR code for URL: %s", request.url)

    # Using keyword arguments
    encoded_url = encode_url_to_filename(request.url)
    qr_filename = f"{encoded_url}.png"
    qr_code_full_path = QR_DIRECTORY / qr_filename

    qr_code_download_url = (
        f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_filename}"
    )

    # Generate HATEOAS links for this resource
    links = [
        generate_links(
            filename=qr_filename,
            base_url=SERVER_BASE_URL,
            download_url=qr_code_download_url
        )
    ]

    # Check if the QR code already exists
    if qr_code_full_path.exists():
        logging.info("QR code already exists.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "QR code already exists.", "links": links}
        )

    # Generate the QR code using keyword arguments
    generate_qr_code(
        data=request.url,
        path=qr_code_full_path,
        fill_color=FILL_COLOR,
        back_color=BACK_COLOR,
        size=request.size
    )

    return QRCodeResponse(
        message="QR code created successfully.",
        qr_code_url=qr_code_download_url,
        links=links
    )

# Define an endpoint to list all QR codes
@router.get("/qr-codes/", response_model=List[QRCodeResponse], tags=["QR Codes"])
async def list_qr_codes_endpoint():
    """
    Lists all QR codes and their download URLs.

    This endpoint retrieves all QR codes stored in the system and returns their
    respective URLs and HATEOAS links.
    """
    logging.info("Listing all QR codes.")

    # Retrieve all QR code files
    qr_files = list_qr_codes(QR_DIRECTORY)

    # Create a response object for each QR code
    responses = [
        QRCodeResponse(
            message="QR code available",
            qr_code_url=decode_filename_to_url(qr_file[:-4]),
            links=generate_links(
                "list", qr_file, SERVER_BASE_URL,
                f"{SERVER_BASE_URL}/{SERVER_DOWNLOAD_FOLDER}/{qr_file}"
            )
        )
        for qr_file in qr_files  # Adjusted to ensure no line is too long
    ]
    return responses

# Define an endpoint to delete a QR code by filename
@router.delete(
    "/qr-codes/{qr_filename}",
    status_code=status.HTTP_200_OK,
    tags=["QR Codes"]
)
async def delete_qr_code_endpoint(qr_filename: str, token: str = Depends(oauth2_scheme)):
    """
    Deletes a QR code by filename. This endpoint deletes the specified QR code if it exists.
    """
    logging.info("Deleting QR code: %s.", qr_filename)
    qr_code_path = QR_DIRECTORY / qr_filename

    if not qr_code_path.is_file():
        logging.warning("QR code not found: %s.", qr_filename)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QR code not found")

    delete_qr_code(qr_code_path)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
