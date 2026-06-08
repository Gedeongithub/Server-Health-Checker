from core.checker import check_all_servers
from core.reporter import generate_report


def main():
    results = check_all_servers()
    generate_report(results)


if __name__ == "__main__":
    main()