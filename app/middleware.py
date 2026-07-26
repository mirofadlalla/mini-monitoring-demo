import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.metrics import (
    ACTIVE_REQUESTS,
    REQUEST_COUNT,
    REQUEST_LATENCY,
)


class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        ACTIVE_REQUESTS.inc()

        start = time.perf_counter()

        try:

            response = await call_next(request)

            return response

        finally:

            duration = time.perf_counter() - start

            endpoint = request.url.path

            status = (
                str(response.status_code)
                if "response" in locals()
                else "500"
            )

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=status,
            ).inc()

            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=endpoint,
            ).observe(duration)

            ACTIVE_REQUESTS.dec()