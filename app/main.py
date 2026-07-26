from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Mini URL Shortener",
)

app.include_router(router)