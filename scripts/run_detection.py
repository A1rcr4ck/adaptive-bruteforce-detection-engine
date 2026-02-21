from core.brute_force_detector import detect_brute_force
from core.spray_detector import detect_password_spray
from core.baseline_detector import detect_anomalies
from core.alert_manager import process_alerts
from core.ip_profile_manager import update_ip_profiles
from core.logger import logger


def run_all_detectors():
    all_alerts = []

    logger.info("Running brute force detector...")
    brute_alerts = detect_brute_force()
    all_alerts.extend(brute_alerts)

    logger.info("Running password spray detector...")
    spray_alerts = detect_password_spray()
    all_alerts.extend(spray_alerts)

    logger.info("Running anomaly detector...")
    anomaly_alerts = detect_anomalies()
    all_alerts.extend(anomaly_alerts)

    logger.info(f"Total alerts detected: {len(all_alerts)}")

    process_alerts(all_alerts)

    update_ip_profiles()


if __name__ == "__main__":
    run_all_detectors()