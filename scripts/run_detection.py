from core.brute_force_detector import detect_brute_force
from core.spray_detector import detect_password_spray
from core.baseline_detector import detect_anomalies
from core.alert_manager import process_alerts
from core.ip_profile_manager import update_ip_profiles


def run_all_detectors():
    all_alerts = []

    print("Running brute force detector...")
    all_alerts.extend(detect_brute_force())

    print("Running password spray detector...")
    all_alerts.extend(detect_password_spray())

    print("Running anomaly detector...")
    all_alerts.extend(detect_anomalies())

    print(f"\nTotal alerts detected: {len(all_alerts)}")

    process_alerts(all_alerts)

    # NEW STEP
    update_ip_profiles()


if __name__ == "__main__":
    run_all_detectors()