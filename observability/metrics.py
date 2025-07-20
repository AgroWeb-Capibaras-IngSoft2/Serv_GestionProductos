from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('productos_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('productos_request_duration_seconds', 'Request latency')
ERROR_COUNT = Counter('productos_errors_total', 'Total errors', ['endpoint'])