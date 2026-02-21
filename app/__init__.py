from flask import Flask, jsonify
from app.routes.api_routes import api_blueprint
from config import APP_NAME, VERSION


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({
            "service": APP_NAME,
            "version": VERSION,
            "status": "running",
            "api_base": "/api"
        })

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app