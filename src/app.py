from flask import Flask

from src.routes.health_routes import health_blueprint
from src.utils.logger_config import (
    logger,
    log_request,
    log_response
)

app = Flask(__name__)

logger.info("Starting Flask REST API server...")


@app.before_request
def before_request_logging():
    log_request()


@app.after_request
def after_request_logging(response):
    log_response({
        "status_code": response.status_code
    })

    return response


# Register routes
app.register_blueprint(health_blueprint)


if __name__ == "__main__":
    logger.info("Application is running on port 5050")

    app.run(
        debug=False,
        use_reloader=False,
        host="0.0.0.0",
        port=5050
    )