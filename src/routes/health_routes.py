from flask import Blueprint, jsonify
from dataclasses import asdict
from datetime import datetime, timezone

from src.models.health_response import HealthResponse
from src.config.settings import (
    APP_VERSION,
    APP_ENVIRONMENT
)

health_blueprint = Blueprint("health", __name__)

@health_blueprint.route("/health", methods=["GET"])
def health():
    response = HealthResponse(
        status="running",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=APP_VERSION,
        environment=APP_ENVIRONMENT
    )
    return jsonify(asdict(response))