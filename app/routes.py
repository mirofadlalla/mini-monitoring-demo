from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.storage import DATABASE, generate_code

from app.metrics import (
    SHORT_URLS_CREATED,
    REDIRECT_COUNT,
)
router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.post("/shorten")
def shorten(request: URLRequest):

    code = generate_code()

    DATABASE[code] = request.url

    SHORT_URLS_CREATED.inc()

    return {
        "short_code": code,
        "short_url": f"http://localhost:8000/{code}",
    }


@router.get("/{code}")
def redirect(code: str):

    if code not in DATABASE:
        raise HTTPException(status_code=404, detail="URL not found")

    REDIRECT_COUNT.inc()
    
    return RedirectResponse(DATABASE[code])


@router.get("/health")
def health():

    return {"status": "healthy"}