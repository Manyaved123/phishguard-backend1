import cv2
import os

REF_FOLDER = "references"


def compare_with_references(filepath):
    try:
        uploaded = cv2.imread(filepath, 0)

        orb = cv2.ORB_create()

        kp1, des1 = orb.detectAndCompute(uploaded, None)

        best_score = 0
        best_match = "Unknown"

        for file in os.listdir(REF_FOLDER):
            ref_path = os.path.join(REF_FOLDER, file)

            ref = cv2.imread(ref_path, 0)

            if ref is None:
                continue

            kp2, des2 = orb.detectAndCompute(ref, None)

            if des1 is None or des2 is None:
                continue

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)

            score = len(matches)

            if score > best_score:
                best_score = score
                best_match = file

        if best_score > 80:
            verdict = "Looks Similar to Official Site"
            risk = 20
        elif best_score > 40:
            verdict = "Possible Clone / Modified Copy"
            risk = 55
        else:
            verdict = "No Trusted Similarity Found"
            risk = 75

        return {
            "similarity_score": best_score,
            "matched_brand": best_match,
            "brand_verdict": verdict,
            "brand_risk": risk
        }

    except Exception as e:
        return {
            "similarity_score": 0,
            "matched_brand": "Error",
            "brand_verdict": str(e),
            "brand_risk": 50
        }