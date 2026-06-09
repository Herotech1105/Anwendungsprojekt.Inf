"""
Run all E2E tests sequentially and print a combined summary.
Usage:  python run_all.py
"""

import subprocess
import sys
from datetime import datetime

TESTS = [
    ("Test 1: Sensor -> DB",           "test_1_sensor_to_db.py"),
    ("Test 2: Keycloak Token Flow",     "test_2_keycloak_token_flow.py"),
    ("Test 3: No Auth Rejected",        "test_3_no_auth_rejected.py"),
    ("Test 4: Invalid Data Rejected",   "test_4_invalid_data_rejected.py"),
    ("Test 5: Actuator Control",        "test_5_actuator_control.py"),
    ("Test 6: TLS Validation",          "test_6_tls_validation.py"),
    ("Test 7: Dashboard Access",        "test_7_dashboard_access.py"),
]

DIVIDER = "=" * 70


def main():
    print(f"\n{DIVIDER}")
    print(f"  E2E TEST SUITE  —  All Tests")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{DIVIDER}\n")

    results = []

    for name, script in TESTS:
        print(f"\n{'#' * 70}")
        print(f"  Running: {name} ({script})")
        print(f"{'#' * 70}")

        proc = subprocess.run(
            [sys.executable, script],
            capture_output=False,
        )

        status = "PASS" if proc.returncode == 0 else "FAIL"
        results.append((name, status))

    # Combined summary
    print(f"\n\n{DIVIDER}")
    print(f"  COMBINED SUMMARY")
    print(f"{DIVIDER}\n")

    passed = sum(1 for _, s in results if s == "PASS")
    failed = sum(1 for _, s in results if s == "FAIL")

    for name, status in results:
        icon = "[PASS]" if status == "PASS" else "[FAIL]"
        print(f"  {icon}  {name}")

    print(f"\n{DIVIDER}")
    print(f"  {passed}/{len(results)} test suites passed, {failed} failed")
    print(f"{DIVIDER}\n")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
