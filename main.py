import json
import sys

from export_service import export_report
from infrai_client import InfraiClient


def main() -> None:
    records = [
        {"event": "build.completed", "release": "2026.09.1", "diagnostic": "all checks green", "occurred_at": "2026-09-09T09:00:00Z"},
        {"event": "release.published", "release": "2026.09.1", "diagnostic": "production", "occurred_at": "2026-09-09T09:04:00Z"},
    ]
    name = sys.argv[1] if len(sys.argv) > 1 else "build-report.csv"
    print(json.dumps({"download_url": export_report(records, InfraiClient(), name)}))


if __name__ == "__main__":
    main()
