from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.storage import DATABASE, generate_code

from app.metrics import (
    SHORT_URLS_CREATED,
    REDIRECT_COUNT,
)

from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from fastapi import Response

'''
generate_latest()
كل الـ Counters والـ Gauges والـ Histograms اللى عرفناها موجودة فى

Collector Registry
وده Registry داخلى فى مكتبة Prometheus.
كل Metric بتعملها بتتسجل فيه تلقائياً.

لما تستدعى
generate_latest()

المكتبة تعمل الآتى
Collector Registry
        │
        ▼
تجمع كل الـ Metrics
        │
        ▼
تحولهم إلى Text Format
        │
        ▼
ترجع Bytes

مثلاً هترجع حاجة شبه
# HELP http_requests_total Total HTTP Requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/health",status="200"} 15
http_request_duration_seconds_bucket{le="0.5"} 10
http_request_duration_seconds_bucket{le="1"} 18
http_request_duration_seconds_sum 3.45
http_request_duration_seconds_count 18
short_urls_created_total 8
وده بالضبط اللى Prometheus بيفهمه.


CONTENT_TYPE_LATEST

لازم الـ Response يبقى

Content-Type:
text/plain; version=0.0.4

وده ثابت اسمه
CONTENT_TYPE_LATEST
'''
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


@router.get("/code/{code}")
def redirect(code: str):

    if code not in DATABASE:
        raise HTTPException(status_code=404, detail="URL not found")

    REDIRECT_COUNT.inc()

    return RedirectResponse(DATABASE[code])


@router.get("/metrics")
def metrics():

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

@router.get("/health")
def health():

    return {"status": "healthy"}