import cv2
import numpy as np


# ==============================
# SAFE IMAGE LOADER
# ==============================
def load(img_path):
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"[HIT ENGINE] Image not found or invalid path: {img_path}")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img, hsv


# ==============================
# COLOR FEATURES
# ==============================

def green_ratio(img_path):
    img, hsv = load(img_path)

    lower = np.array([30, 40, 40])
    upper = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    return float(np.sum(mask > 0) / mask.size)


def brown_ratio(img_path):
    img, hsv = load(img_path)

    lower = np.array([8, 60, 20])
    upper = np.array([25, 255, 150])

    mask = cv2.inRange(hsv, lower, upper)
    return float(np.sum(mask > 0) / mask.size)


def red_ratio(img_path):
    img, hsv = load(img_path)

    lower1 = np.array([0, 80, 40])
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([160, 80, 40])
    upper2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower1, upper1) + \
           cv2.inRange(hsv, lower2, upper2)

    return float(np.sum(mask > 0) / mask.size)


# ==============================
# TEXTURE FEATURE
# ==============================

def spot_density(img_path):
    img, _ = load(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 40, 120)

    return float(np.sum(edges > 0) / edges.size)


# ==============================
# HIT RULE ENGINE
# ==============================

def hit_rules(img_path):

    g = green_ratio(img_path)
    b = brown_ratio(img_path)
    r = red_ratio(img_path)
    s = spot_density(img_path)

    # ----- RULE BASED LOGIC -----

    if g > 0.55 and s < 0.08:
        disease = "healthy"
        conf = 70 + (g * 30)

    elif b > 0.25:
        disease = "brown blight"
        conf = 60 + (b * 40)

    elif r > 0.20:
        disease = "red rust"
        conf = 60 + (r * 40)

    elif s > 0.15:
        disease = "blister blight"
        conf = 55 + (s * 45)

    else:
        disease = "unknown"
        conf = 40

    return {
        "hit_disease": disease,
        "hit_confidence": round(conf, 2),
        "features": {
            "green_ratio": round(g, 3),
            "brown_ratio": round(b, 3),
            "red_ratio": round(r, 3),
            "spot_density": round(s, 3)
        }
    }