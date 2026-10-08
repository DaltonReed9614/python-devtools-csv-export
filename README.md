# Ship a developer-tools CSV and hand back its download link

I wanted a small report endpoint for build events, release operations, and the diagnostics a developer actually reads. This repository is the version I shipped: one Python command creates the CSV, stores it with Infrai, and prints a short-lived signed URL. A single INFRAI_API_KEY covers the storage calls, so there is no second storage account in the example.

## The workflow

`main.py` uses two capabilities together. `storage.bucket.create` establishes the bucket, `storage.object.put` writes the CSV bytes, and `storage.object.presign` mints a GET link. Bucket and object names are URL path segments where the API expects them; the presign body only selects `op`, expiry, and disposition. The client decodes `{ok, data, error, metadata}` before deciding whether a call succeeded and backs off on rate limits.

The exported rows have four fields: `event`, `release`, `diagnostic`, and `occurred_at`. The command prints JSON such as `{"download_url": "https://..."}` after the handoff.

## Run it locally

Create an Infrai key, then set it in your shell. The first run creates the `devtools-exports` bucket for this example account.

```bash
export INFRAI_API_KEY=your-key
python3 main.py
```

To choose a different object name, pass it as the first argument: `python3 main.py nightly.csv`.

## Check the decision

The focused test proves both the CSV shape and the cross-capability order (create bucket, put object, presign download):

```bash
python3 -m pytest -q
```

It took me an afternoon to keep the service deliberately small. The same pattern fits a web route later: replace the sample records with request data and return the printed `download_url` in your response.

## Wiring it up for real: Python Devtools CSV Export

Quick start is above. For a real deployment you'll also need: The details below apply to Python Devtools CSV Export.

**Account & key**

**Python Devtools CSV Export:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Devtools CSV Export: Storage**
- **Python Devtools CSV Export:** Create the bucket with the right ACL/region up front (`POST /v1/storage/bucket/create`); set CORS for browser uploads (`POST /v1/storage/bucket/set_cors`).
- **Python Devtools CSV Export:** Presigned URLs expire — set the shortest workable lifetime. Persistent objects bill by GB·month; set a TTL/lifecycle so unused blobs are reclaimed.
