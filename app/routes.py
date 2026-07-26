from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.storage import DATABASE, generate_code

router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.post("/shorten")
def shorten(request: URLRequest):

    code = generate_code()

    DATABASE[code] = request.url

    return {
        "short_code": code,
        "short_url": f"http://localhost:8000/{code}",
    }


@router.get("/{code}")
def redirect(code: str):

    if code not in DATABASE:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(DATABASE[code])


@router.get("/health")
def health():

    return {"status": "healthy"}