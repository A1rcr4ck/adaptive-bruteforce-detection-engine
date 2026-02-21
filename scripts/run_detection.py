from datetime import datetime
from core.brute_force_detector import detect_brute_force
from core.spray_detector import detect_password_spray
from core.baseline_detector import detect_anomalies
from core.alert_manager import process_alerts
from core.ip_profile_manager import update_ip_profiles
from core.logger import logger


def run_all_detectors():
    start_time = datetime.now()
    logger.info("Detection pipeline started.")

    all_alerts = []

    brute_alerts = detect_brute_force()
    spray_alerts = detect_password_spray()
    anomaly_alerts = detect_anomalies()

    all_alerts.extend(brute_alerts)
    all_alerts.extend(spray_alerts)
    all_alerts.extend(anomaly_alerts)

    logger.info(f"Brute force alerts: {len(brute_alerts)}")
    logger.info(f"Password spray alerts: {len(spray_alerts)}")
    logger.info(f"Anomaly alerts: {len(anomaly_alerts)}")
    logger.info(f"Total alerts detected: {len(all_alerts)}")

    process_alerts(all_alerts)
    update_ip_profiles()

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    logger.info(f"Detection pipeline completed in {duration:.2f} seconds.")


if __name__ == "__main__":
    run_all_detectors()