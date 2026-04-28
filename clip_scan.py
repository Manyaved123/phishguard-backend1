from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Load model once
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def analyze_clip(filepath):
    try:
        image = Image.open(filepath).convert("RGB")

        labels = [
            "a legitimate professional website homepage",
            "a phishing login page",
            "a fake banking verification page",
            "a scam payment form",
            "a secure trusted website"
        ]

        inputs = processor(
            text=labels,
            images=image,
            return_tensors="pt",
            padding=True
        )

        outputs = model(**inputs)
        logits = outputs.logits_per_image
        probs = logits.softmax(dim=1)[0]

        scores = probs.tolist()

        phishing_score = (
            scores[1] + scores[2] + scores[3]
        ) * 100

        if phishing_score >= 70:
            verdict = "High Risk"
        elif phishing_score >= 40:
            verdict = "Medium Risk"
        else:
            verdict = "Low Risk"

        return {
            "clip_score": round(phishing_score, 2),
            "verdict": verdict,
            "labels": {
                labels[i]: round(scores[i] * 100, 2)
                for i in range(len(labels))
            }
        }

    except Exception as e:
        return {
            "clip_score": 0,
            "verdict": "Error",
            "labels": {"error": str(e)}
        }