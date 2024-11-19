"""
This module contains the OAuth2 routes and logic for authentication, token generation, and security.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.common import authenticate_user, create_access_token

router = APIRouter()

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    This function is responsible for generating an access token after authenticating the user.
    It uses the provided credentials to verify the user and returns a JWT access token.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}
