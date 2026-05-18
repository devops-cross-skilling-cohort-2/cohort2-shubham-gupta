from flask import Flask, jsonify
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

app = Flask(__name__)


@dataclass
class HealthResponse:
    status: str
    timestamp: str
    version: str
    environment: str


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

    app.run(
        debug=False,
        use_reloader=False,
        host="0.0.0.0",
        port=5050
    )