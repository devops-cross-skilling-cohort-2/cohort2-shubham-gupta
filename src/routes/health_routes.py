from flask import Blueprint, jsonify
from dataclasses import asdict
from datetime import datetime, timezone

from src.models.health_response import HealthResponse

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health():
    response = HealthResponse(
        status="running",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.0.0",
        environment="dev"
    )

    return jsonify(asdict(response))