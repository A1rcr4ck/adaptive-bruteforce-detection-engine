from flask import Blueprint, jsonify
from flask import request
from core.health_check import run_health_check
from app.services.query_service import (
    get_overview_stats,
    get_all_alerts,
    get_alert_by_id,
    resolve_alert
)
from app.services.analytics_service import (
    get_failed_trend,
    get_top_ips,
    get_attack_distribution,
    get_ip_profile
)
from app.services.analytics_service import get_overview_detailed
from app.services.analytics_service import get_alert_investigation
from app.services.analytics_service import get_top_users
from app.services.analytics_service import get_threat_intel

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def api_root():
    return jsonify({
        "message": "Adaptive Brute-Force Detection Engine API",
        "available_endpoints": [
            "/api/health",
            "/api/overview",
            "/api/alerts",
            "/api/alert/<id>",
            "/api/resolve/<id>"
        ]
    })


@api_blueprint.route("/health", methods=["GET"])
def health():
    return jsonify(run_health_check())


@api_blueprint.route("/overview", methods=["GET"])
def overview():
    return jsonify(get_overview_stats())


# @api_blueprint.route("/alerts", methods=["GET"])
# def alerts():
#     return jsonify(get_all_alerts())


@api_blueprint.route("/alert/<int:alert_id>", methods=["GET"])
def alert_detail(alert_id):
    return jsonify(get_alert_by_id(alert_id))


@api_blueprint.route("/resolve/<int:alert_id>", methods=["POST"])
def resolve(alert_id):
    return jsonify(resolve_alert(alert_id))

@api_blueprint.route("/failed-trend", methods=["GET"])
def failed_trend():
    return jsonify(get_failed_trend())


@api_blueprint.route("/top-ips", methods=["GET"])
def top_ips():
    return jsonify(get_top_ips())


@api_blueprint.route("/attack-distribution", methods=["GET"])
def attack_distribution():
    return jsonify(get_attack_distribution())


@api_blueprint.route("/ip-profile/<ip>", methods=["GET"])
def ip_profile(ip):
    return jsonify(get_ip_profile(ip))

@api_blueprint.route("/alerts", methods=["GET"])
def alerts():
    filters = {}

    severity = request.args.get("severity")
    status = request.args.get("status")
    attack_type = request.args.get("attack_type")
    ip = request.args.get("ip")

    if severity:
        filters["severity"] = severity

    if status:
        filters["status"] = status

    if attack_type:
        filters["attack_type"] = attack_type

    if ip:
        filters["ip"] = ip

    return jsonify(get_all_alerts(filters))

@api_blueprint.route("/overview-detailed", methods=["GET"])
def overview_detailed():
    return jsonify(get_overview_detailed())

@api_blueprint.route("/investigation/<int:alert_id>", methods=["GET"])
def investigation_data(alert_id):
    return jsonify(get_alert_investigation(alert_id))

@api_blueprint.route("/top-users", methods=["GET"])
def top_users():
    return jsonify(get_top_users())

@api_blueprint.route("/threat-intel/<ip>", methods=["GET"])
def threat_intel(ip):
    return jsonify(get_threat_intel(ip))
