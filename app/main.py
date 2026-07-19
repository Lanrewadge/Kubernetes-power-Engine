from flask import Flask, jsonify, Response
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

HTTP_REQUESTS = Counter(
    "flask_http_request_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
HTTP_EXCEPTIONS = Counter(
    "flask_http_request_exceptions_total",
    "Total exceptions while handling requests",
)
REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
)


def instrumented(handler, endpoint_name):
    start = time.time()
    status = 500
    try:
        payload, status = handler()
        return payload, status
    except Exception:
        HTTP_EXCEPTIONS.inc()
        raise
    finally:
        elapsed = time.time() - start
        REQUEST_LATENCY.labels(endpoint=endpoint_name).observe(elapsed)
        HTTP_REQUESTS.labels(method="GET", endpoint=endpoint_name, status=str(status)).inc()


@app.get("/healthz")
def healthz():
    return instrumented(lambda: (jsonify(status="ok"), 200), "/healthz")


@app.get("/readyz")
def readyz():
    return instrumented(lambda: (jsonify(ready=True), 200), "/readyz")


@app.get("/")
def root():
    def response():
        env = os.getenv("APP_ENV", "unknown")
        version = os.getenv("APP_VERSION", "v1")
        return (
            jsonify(
                app="kubernetes-power-engine",
                message="Advanced Kubernetes baseline is running",
                environment=env,
                version=version,
            ),
            200,
        )

    return instrumented(response, "/")


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
