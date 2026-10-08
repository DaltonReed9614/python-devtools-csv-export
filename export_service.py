import csv
import io
import uuid
from typing import Iterable, Mapping, Any, TypedDict

from infrai_client import InfraiClient

BUCKET = "devtools-exports"


class ExportRecord(TypedDict, total=False):
    event: str
    release: str
    diagnostic: str
    occurred_at: str


def build_csv(records: Iterable[ExportRecord]) -> bytes:
    columns = ["event", "release", "diagnostic", "occurred_at"]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue().encode("utf-8")


def export_report(records: Iterable[ExportRecord], client: InfraiClient, report_name: str = "build-report.csv") -> str:
    data = build_csv(records)
    client.create_bucket(BUCKET)
    client.put_object(BUCKET, report_name, data, "text/csv", f"export-{uuid.uuid4()}")
    # This is the storage.object.presign handoff from writing to downloading.
    signed = client.presign_download(BUCKET, report_name)
    return signed["url"]
