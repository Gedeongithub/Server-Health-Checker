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