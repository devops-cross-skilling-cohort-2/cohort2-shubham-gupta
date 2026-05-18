from flask import Flask, jsonify
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

from logger_config import logger, log_request, log_response

app = Flask(__name__)


@dataclass
class HealthResponse:
    status: str
    timestamp: str
    version: str
    environment: str


logger.info("Starting Flask REST API server...")


# Logs ALL incoming requests
@app.before_request
def before_request_logging():
    log_request()


# Logs ALL outgoing responses
@app.after_request
def after_request_logging(response):
    log_response({
        "status_code": response.status_code
    })
    return response


@app.route("/health", methods=["GET"])
def health():
    response = HealthResponse(
        status="running",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.0.0",
        environment="dev"
    )

    return jsonify(asdict(response))


if __name__ == "__main__":
    logger.info("Application is running on port 5050")

    app.run(
        debug=False,
        use_reloader=False,
        host="0.0.0.0",
        port=5050
    )