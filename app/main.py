from fastapi import FastAPI

from app.routes import router
from app.middleware import MetricsMiddleware

app = FastAPI(
    title="Mini URL Shortener",
)
app.add_middleware(MetricsMiddleware)
app.include_router(router)