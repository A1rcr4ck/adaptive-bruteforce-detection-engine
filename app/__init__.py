from flask import Flask, render_template
from app.routes.api_routes import api_blueprint
from config import APP_NAME, VERSION


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        return render_template("overview.html")

    @app.route("/analytics")
    def analytics():
        return render_template("analytics.html")

    @app.route("/investigation")
    def investigation():
        return render_template("investigation.html")

    @app.route("/threat-intel")
    def threat_intel():
        return render_template("threat_intel.html")

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app