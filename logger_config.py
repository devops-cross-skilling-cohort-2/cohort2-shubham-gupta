# logger_config.py
import json
import logging
from datetime import datetime, timezone
from flask import request


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )

    logger = logging.getLogger("health-api")

    # Disable default Flask/Werkzeug logs
    logging.getLogger("werkzeug").disabled = True

    return logger


logger = setup_logger()


def current_timestamp():
    return datetime.now(timezone.utc).isoformat()


def log_request():
    log_data = {
        "timestamp": current_timestamp(),
        "event": "api_request",
        "method": request.method,
        "path": request.path,
        "client_ip": request.remote_addr
    }

    logger.info(json.dumps(log_data))


def log_response(response_data):
    log_data = {
        "timestamp": current_timestamp(),
        "event": "api_response",
        "response": response_data
    }

    logger.info(json.dumps(log_data))