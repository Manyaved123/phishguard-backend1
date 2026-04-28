from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from similarity_scan import compare_with_references
import joblib

#from image_match import analyze_image
#from clip_scan import analyze_clip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
url_model = joblib.load("live_url_model.pkl")
text_model = joblib.load("text_model_advanced.pkl")


# ---------------- REQUEST MODELS ----------------
class URLRequest(BaseModel):
    url: str


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "PhishGuard AI Advanced Hybrid Running"}


# ---------------- URL MODEL ----------------
def extract(url):
    url = url.lower()

    return [[
        len(url),
        url.count("."),
        url.count("-"),
        url.count("@"),
        1 if "login" in url else 0,
        1 if "verify" in url else 0,
        1 if "bank" in url else 0,
        1 if url.startswith("http://") else 0
    ]]


@app.post("/scan-url")
def scan_url(data: URLRequest):
    pred = url_model.predict(extract(data.url))[0]

    if pred == 1:
        return {
            "risk_score": 90,
            "verdict": "High Risk",
            "reasons": ["ML model detected phishing URL"]
        }

    return {
        "risk_score": 12,
        "verdict": "Low Risk",
        "reasons": ["URL appears safer"]
    }


# ---------------- TEXT MODEL ----------------
@app.post("/scan-text")
def scan_text(data: TextRequest):
    pred = text_model.predict([data.text])[0]

    if pred == 1:
        return {
            "risk_score": 88,
            "verdict": "High Risk",
            "reasons": ["NLP model detected phishing intent"]
        }

    return {
        "risk_score": 15,
        "verdict": "Low Risk",
        "reasons": ["Message appears safer"]
    }


# ---------------- IMAGE MODEL ----------------
@app.post("/scan-image")
def scan_image():
    return {
        "risk_score": 45,
        "verdict": "Medium Risk",
        "reasons": ["Image scanning module temporarily simplified for deployment"]
    }
