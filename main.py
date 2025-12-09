import argparse
import sys
import csv
from tabulate import tabulate
from reports.performance import PerformanceReport

AVAILABLE_REPORTS = {
    "performance": PerformanceReport,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="CSV report generator: combine files and render report"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV files (one or more)"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Report name (e.g., 'performance')"
    )
    return parser.parse_args()


def read_csv_files(paths):
    rows = []
    for path in paths:
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                # Валидация заголовков (минимальный набор)
                required = {"name", "position", "completed_tasks", "performance", "skills", "team", "experience_years"}
                if not required.issubset(set(reader.fieldnames or [])):
                    raise ValueError(f"File '{path}' has invalid headers. Expected at least: {required}")
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            print(f"Error: file '{path}' not found.", file=sys.stderr)
            sys.exit(2)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)
    return rows


def main():
    args = parse_args()

    report_name = args.report.strip().lower()
    if report_name not in AVAILABLE_REPORTS:
        print(f"Error: report '{args.report}' is not supported. Available: {', '.join(AVAILABLE_REPORTS.keys())}", file=sys.stderr)
        sys.exit(2)

    data = read_csv_files(args.files)
    report_cls = AVAILABLE_REPORTS[report_name]
    report = report_cls()
    table_rows, headers = report.generate(data)

    print(tabulate(table_rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
