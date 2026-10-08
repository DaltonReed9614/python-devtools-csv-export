import json

from export_service import build_csv, export_report


class FakeClient:
    def __init__(self):
        self.calls = []

    def create_bucket(self, name):
        self.calls.append(("create", name))

    def put_object(self, bucket, key, data, content_type, idempotency_key):
        self.calls.append(("put", bucket, key, data, content_type, idempotency_key))

    def presign_download(self, bucket, key):
        self.calls.append(("presign", bucket, key))
        return {"url": "https://download.example/report.csv"}


def test_csv_and_handoff_order():
    rows = [{"event": "build.completed", "release": "r1", "diagnostic": "ok", "occurred_at": "now"}]
    assert build_csv(rows).decode() == "event,release,diagnostic,occurred_at\nbuild.completed,r1,ok,now\n"
    client = FakeClient()
    assert export_report(rows, client) == "https://download.example/report.csv"
    assert [call[0] for call in client.calls] == ["create", "put", "presign"]
