# PhishGuard AI: Backend API (deployment build with image scanning)

A FastAPI backend that serves **PhishGuard AI's** phishing-detection models, packaged for cloud deployment (Python 3.10, see `runtime.txt`). Compared with [phishguard-backend](https://github.com/Manyaved123/phishguard-backend), it includes the visual-similarity modules and an image-scan endpoint.

➡️ **Full project** (frontend, browser extension, dashboard): [PHISHGUARD-AI-CIPHERIX](https://github.com/Manyaved123/PHISHGUARD-AI-CIPHERIX)

## Endpoints

| Method | Route | Input | What it does |
|---|---|---|---|
| `GET` | `/` | – | Health check |
| `POST` | `/scan-url` | `{"url": "..."}` | URL phishing classifier (lexical features) |
| `POST` | `/scan-text` | `{"text": "..."}` | NLP classifier for phishing messages |
| `POST` | `/scan-image` | – | Placeholder: returns a fixed "Medium Risk" response in this deployment build |

Response format:
```json
{"risk_score": 88, "verdict": "High Risk", "reasons": ["NLP model detected phishing intent"]}
```

## Visual clone-detection modules

These are included in the repo but not yet wired into `/scan-image` in this build:

- `similarity_scan.py`: **ORB keypoint matching** of a screenshot against reference pages of real brands (`sbi.png`, `paypal.png`, `amazon.png`), to catch look-alike login pages.
- `image_match.py`, `clip_scan.py`: alternative image-matching approaches, including CLIP embeddings.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# API docs: http://127.0.0.1:8000/docs
```

## Tech

Python 3.10 · FastAPI · scikit-learn · OpenCV (ORB) · joblib
