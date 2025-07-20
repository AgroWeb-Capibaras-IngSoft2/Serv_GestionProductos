import time
from functools import wraps
from flask import request
from observability.metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT

def monitor_endpoint(endpoint_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint_name).inc()
            try:
                response = func(*args, **kwargs)
                REQUEST_LATENCY.observe(time.time() - start_time)
                status_code = 200
                if isinstance(response, tuple) and len(response) >= 2:
                    status_code = response[1]
                if status_code >= 400:
                    ERROR_COUNT.labels(endpoint=endpoint_name).inc()
                return response
            except Exception as e:
                ERROR_COUNT.labels(endpoint=endpoint_name).inc()
                REQUEST_LATENCY.observe(time.time() - start_time)
                raise e
        return wrapper
    return decorator