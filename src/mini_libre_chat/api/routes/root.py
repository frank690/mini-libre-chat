"""
Root API Route. This module defines the API route for the root endpoint.
"""

__all__ = ["router"]

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def root():
    return RedirectResponse("/app")
