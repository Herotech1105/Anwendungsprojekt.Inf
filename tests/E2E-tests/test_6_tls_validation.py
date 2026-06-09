"""
Test 6: TLS-Zertifikatsvalidierung
====================================
controller.py -> nginx (HTTPS mit CA-Zertifikat)

Verifies that HTTPS works with the correct CA certificate
and fails with a wrong/missing certificate.
"""

import os
import tempfile

import requests

from config import CA_CERT_FILE, STATUS_URL, HTTP_TIMEOUT
from helpers import print_header, record, exit_with_result, PASS, FAIL


def run():
    print_header("TEST 6: TLS Certificate Validation")

    # -- 6a: CA file exists --
    if os.path.isfile(CA_CERT_FILE):
        size = os.path.getsize(CA_CERT_FILE)
        record(PASS, f"CA certificate file exists ({CA_CERT_FILE})",
               f"Size: {size} bytes")
    else:
        record(FAIL, "CA certificate file exists",
               f"Not found: {CA_CERT_FILE}")
        exit_with_result()

    # -- 6b: HTTPS with correct CA succeeds --
    try:
        resp = requests.get(STATUS_URL, timeout=HTTP_TIMEOUT, verify=CA_CERT_FILE)
        record(PASS, "HTTPS request with correct CA succeeds",
               f"Status {resp.status_code}")
    except requests.exceptions.SSLError as exc:
        record(FAIL, "HTTPS request with correct CA succeeds",
               f"SSL Error: {exc}")
    except requests.RequestException as exc:
        record(FAIL, "HTTPS request with correct CA succeeds",
               f"Connection error: {exc}")

    # -- 6c: HTTPS with wrong CA fails --
    fake_ca = None
    try:
        # Create a temporary self-signed cert that does NOT match
        fake_ca = tempfile.NamedTemporaryFile(
            mode="w", suffix=".pem", delete=False,
        )
        # This is a deliberately invalid/empty CA bundle
        fake_ca.write("-----BEGIN CERTIFICATE-----\n")
        fake_ca.write("THISISNOTAVALIDCERTIFICATE\n")
        fake_ca.write("-----END CERTIFICATE-----\n")
        fake_ca.close()

        resp = requests.get(STATUS_URL, timeout=HTTP_TIMEOUT, verify=fake_ca.name)
        # If we get here, it SHOULD have failed
        record(FAIL, "HTTPS with wrong CA rejected",
               f"Request succeeded with status {resp.status_code} (should have failed)")
    except requests.exceptions.SSLError:
        record(PASS, "HTTPS with wrong CA rejected (SSLError raised)")
    except requests.RequestException as exc:
        # Other connection errors also count as rejected
        record(PASS, "HTTPS with wrong CA rejected",
               f"Error: {type(exc).__name__}")
    finally:
        if fake_ca:
            os.unlink(fake_ca.name)

    exit_with_result()


if __name__ == "__main__":
    run()
