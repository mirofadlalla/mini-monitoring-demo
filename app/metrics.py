from prometheus_client import Counter, Gauge, Histogram

# إجمالى عدد الـ Requests
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"],
)


# عدد الـ Requests الحالية
ACTIVE_REQUESTS = Gauge(
    "http_active_requests",
    "Current Active HTTP Requests",
)

# زمن تنفيذ الـ Request
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"],
    buckets=(
        0.01,
        0.05,
        0.1,
        0.25,
        0.5,
        1,
        2.5,
        5,
        10,
    ),
)

# عدد الروابط المختصرة التى تم إنشاؤها
SHORT_URLS_CREATED = Counter(
    "short_urls_created_total",
    "Total Short URLs Created",
)

# عدد الـ Redirects
REDIRECT_COUNT = Counter(
    "redirects_total",
    "Total Redirects",
)