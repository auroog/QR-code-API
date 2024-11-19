"""
This module provides functions to list, generate, and delete QR code images,
as well as create directories for saving QR codes. The QR codes are saved as PNG
images and stored at a specified file path.
"""

import logging
import os
from pathlib import Path
from typing import List
import qrcode


def list_qr_codes(directory_path: Path) -> List[str]:
    """
    Lists all QR code images in the specified directory by returning their filenames.

    Parameters:
    - directory_path (Path): The filesystem path to the directory containing QR code images.

    Returns:
    - A list of filenames (str) for QR codes found in the directory.
    """
    try:
        # List all files ending with '.png' in the specified directory.
        return [
            f for f in os.listdir(directory_path) if f.endswith('.png')
        ]
    except FileNotFoundError:
        logging.error("Directory not found: %s", directory_path)
        raise
    except OSError as e:
        logging.error("An OS error occurred while listing QR codes: %s", e)
        raise


def generate_qr_code(data: str, path: Path, fill_color: str = 'red',
                     back_color: str = 'white', size: int = 10):
    """
    Generates a QR code based on the provided data and saves it to a specified file path.

    Parameters:
    - data (str): The data to encode in the QR code.
    - path (Path): The filesystem path where the QR code image will be saved.
    - fill_color (str): Color of the QR code.
    - back_color (str): Background color of the QR code.
    - size (int): The size of each box in the QR code grid.
    """
    logging.debug("QR code generation started")
    try:
        qr = qrcode.QRCode(version=1, box_size=size, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(str(path))
        logging.info(
            "QR code successfully saved to %s", path
        )
    except Exception as e:
        logging.error(
            "Failed to generate/save QR code: %s", e
        )
        raise


def delete_qr_code(file_path: Path):
    """
    Deletes the specified QR code image file.

    Parameters:
    - file_path (Path): The filesystem path of the QR code image to delete.
    """
    if file_path.is_file():
        file_path.unlink()
        logging.info(
            "QR code %s deleted successfully", file_path.name
        )
    else:
        logging.error(
            "QR code %s not found for deletion", file_path.name
        )
        raise FileNotFoundError(
            f"QR code {file_path.name} not found"
        )


def create_directory(directory_path: Path):
    """
    Creates a directory at the specified path if it doesn't already exist.

    Parameters:
    - directory_path (Path): The filesystem path of the directory to create.
    """
    logging.debug("Attempting to create directory")
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        logging.info(
            "Directory already exists: %s", directory_path
        )
    except PermissionError as e:
        logging.error(
            "Permission denied when trying to create directory %s: %s", directory_path, e
        )
        raise
    except Exception as e:
        logging.error(
            "Unexpected error creating directory %s: %s", directory_path, e
        )
        raise
