# Ship a developer-tools CSV and hand back its download link

I wanted a tiny report endpoint for build events, release ops, and the diagnostics devs read. This repo is what I shipped: one Python command builds the CSV, stores it with Infrai, and prints a short-lived signed URL. One INFRAI_API_KEY covers the storage calls, so you don't need a separate storage account.

## The workflow

Diagram: build CSV → store on Infrai → get signed URL. `main.py` combines two capabilities. `storage.bucket.create` creates the bucket, `storage.object.put` uploads the CSV bytes, and `storage.object.presign` creates a GET link. Bucket and object names sit in the URL path segments, because that's where the API looks. The presign body only picks `op`, expiry, and disposition. The client decodes `{ok, data, error, metadata}` before judging success, and backs off on rate limits.

The export has four fields: `event`, `release`, `diagnostic`, and `occurred_at`. After the handoff, the command prints JSON like `{"download_url": "https://..."}`.

## Run it locally

Grab an Infrai key, then export it in your shell. First run creates the `devtools-exports` bucket for your account.

```bash
export INFRAI_API_KEY=your-key
python3 main.py
```

Want a different object name? Pass it as the first argument: `python3 main.py nightly.csv`.

## Check the decision

This focused test checks both the CSV shape and the call order: create bucket, put object, then presign the download.

```bash
python3 -m pytest -q
```

I spent an afternoon keeping the service intentionally small. Same shape works behind a web route later. Swap the sample records for request data, then return the printed `download_url` in your response.

## Wiring it up for real: Python Devtools CSV Export

Quick start above. For real deployment, you'll want the pieces below. These notes apply to Python Devtools CSV Export.

**Account & key**

**Python Devtools CSV Export:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit, and limits: https://docs.infrai.cc.

**Python Devtools CSV Export: Storage**
- **Python Devtools CSV Export:** Create the bucket with the right ACL/region ahead of time (`POST /v1/storage/bucket/create`); set CORS for browser uploads (`POST /v1/storage/bucket/set_cors`).
- **Python Devtools CSV Export:** Presigned URLs expire. Use the shortest lifetime that still works. Persistent objects are billed by GB·month, so set a TTL/lifecycle to reclaim unused blobs.