import time
import requests
from utils.logger import get_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.config_loader import load_servers

logger = get_logger()

SLOW_THRESHOLD_MS = 500


def check_server(url: str):
    """
    Check a single server's health:
    - HTTP status
    - response time
    - JSON validation
    - slow detection
    """

    start_time = time.time()

    try:
        res = requests.get(url, timeout=5)

        end_time = time.time()
        duration_ms = int((end_time - start_time) * 1000)

        status_code = res.status_code

        # -------------------------
        # JSON VALIDATION
        # -------------------------
        json_valid = False
        data = None

        try:
            data = res.json()

            if isinstance(data, dict) and data.get("status") == "ok":
                json_valid = True
                logger.info(f"VALID JSON STATUS OK: {url}")

        except ValueError:
            # Not JSON response
            json_valid = False

        # -------------------------
        # HEALTH CLASSIFICATION
        # -------------------------
        if 200 <= status_code < 300 and json_valid:
            status = "HEALTHY"
        elif 200 <= status_code < 300:
            status = "UNSTABLE"
        else:
            status = "DOWN"

        # -------------------------
        # SLOW CHECK
        # -------------------------
        slow = False
        if duration_ms > SLOW_THRESHOLD_MS:
            slow = True
            logger.warning(f"SLOW SERVICE: {url} -> {duration_ms}ms")

        # -------------------------
        # LOG RESULT
        # -------------------------
        logger.info(f"{url} -> {status_code} in {duration_ms}ms [{status}]")

        return {
            "url": url,
            "status_code": status_code,
            "response_time_ms": duration_ms,
            "status": status,
            "json_valid": json_valid,
            "slow": slow
        }

    except requests.exceptions.Timeout:
        logger.error(f"TIMEOUT: {url}")

        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "status": "TIMEOUT",
            "json_valid": False,
            "slow": True
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"ERROR: {url} -> {str(e)}")

        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "status": "ERROR",
            "json_valid": False,
            "slow": False
        }
        
        
# ==================================
# CHECKING ALL SERVERS
# ==================================

def check_all_servers():
    """
    Run all server checks in parallel.
    """

    servers = load_servers()
    results = []

    logger.info(f"Starting health checks for {len(servers)} servers")

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {
            executor.submit(check_server, url): url for url in servers
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]

            try:
                result = future.result()
                results.append(result)

            except Exception as e:
                logger.error(f"FAILED CHECK: {url} -> {str(e)}")

                results.append({
                    "url": url,
                    "status": "ERROR",
                    "status_code": None,
                    "response_time_ms": None,
                    "json_valid": False,
                    "slow": False
                })

    logger.info("All server checks completed")

    return results


# ==============================
# REPORTING
# ===========================

def format_result(result: dict) -> str:
    """
    Format a single server result into a readable line.
    """

    url = result.get("url")
    status = result.get("status")
    code = result.get("status_code")
    time_ms = result.get("response_time_ms")
    slow = result.get("slow")

    line = f"{url:<30} — {status}"

    if code is not None:
        line += f" ({code})"

    if time_ms is not None:
        line += f" — {time_ms}ms"

    if slow:
        line += "  [SLOW]"

    return line


def generate_report(results: list[dict]) -> dict:
    """
    Generate final summary report.
    """

    failed = []

    print("\n--- SERVICE REPORT ---\n")

    for r in results:
        print(format_result(r))

        if r.get("status") in ["DOWN", "ERROR", "TIMEOUT"]:
            failed.append(r["url"])

    print("\n--- SUMMARY ---")

    if failed:
        print(f"Failed services: {', '.join(failed)}")
    else:
        print("All services are healthy")

    return {
        "failed_services": failed,
        "total": len(results),
        "failed_count": len(failed)
    }