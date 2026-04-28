import pytesseract
from PIL import Image, ImageFilter, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def analyze_image(filepath):
    try:
        risk = 0
        reasons = []

        img = Image.open(filepath)

        # Resize for OCR
        img = img.resize((img.width * 2, img.height * 2))

        # Convert grayscale
        img = img.convert("L")

        # Sharpen
        img = img.filter(ImageFilter.SHARPEN)

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)

        # OCR
        text = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 6"
        )

        text_lower = text.lower()

        reasons.append("OCR text extracted")

        keywords = [
            "login", "verify", "bank", "password",
            "otp", "account", "urgent", "reward",
            "free", "wallet", "kyc", "payment",
            "card number", "security code",
            "shipping address", "continue"
        ]

        for word in keywords:
            if word in text_lower:
                risk += 12
                reasons.append(f"Detected '{word}'")

        if "http" in text_lower or ".com" in text_lower:
            risk += 15
            reasons.append("URL detected")

        if "card number" in text_lower:
            risk += 20

        if "security code" in text_lower:
            risk += 20

        if risk >= 70:
            verdict = "High Risk"
        elif risk >= 40:
            verdict = "Medium Risk"
        else:
            verdict = "Low Risk"

        return {
            "risk_score": min(risk, 100),
            "verdict": verdict,
            "reasons": reasons,
            "extracted_text": text[:500]
        }

    except Exception as e:
        return {
            "risk_score": 0,
            "verdict": "Error",
            "reasons": [str(e)]
        }