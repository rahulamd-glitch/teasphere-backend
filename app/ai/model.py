import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

from app.utils.hit_engine import hit_rules
from app.ai.fusion import fuse_decision


# =====================================================
# 1. MODEL LOADING (Finetuned → Fallback)
# =====================================================

try:
    MODEL_PATH = "models/tea_leaf_model_finetuned.keras"
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Loaded FINETUNED model")

except Exception as e:
    print("⚠ Finetuned model not found, loading base model:", e)

    MODEL_PATH = "models/tea_leaf_model.keras"
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Loaded BASE model")


# =====================================================
# 2. CLASS ORDER (MUST MATCH TRAINING GENERATOR)
# =====================================================

CLASS_ORDER = [
    "blister blight",
    "brown blight",
    "healthy",
    "red rust"
]


# =====================================================
# 3. SEVERITY LOGIC
# =====================================================

def get_severity(confidence):
    if confidence > 85:
        return "High"
    elif confidence > 60:
        return "Medium"
    else:
        return "Low"


# =====================================================
# 4. TREATMENT GUIDE
# =====================================================

TREATMENT_GUIDE = {
    "blister blight": [
    "Use Mancozeb 75% WP / ম্যানকোজেব ৭৫% WP ব্যৱহাৰ কৰক",
    "Prune affected branches / আক্ৰান্ত ডাল-পাত কাটি পেলাওক",
    "Avoid excess nitrogen / অতিৰিক্ত নাইট্ৰোজেন ব্যৱহাৰ এৰাই চলক"
],

"brown blight": [
    "Apply Copper Oxychloride 0.3% / কপাৰ অক্সিক্লোৰাইড ০.৩% প্ৰয়োগ কৰক",
    "Remove infected leaves / আক্ৰান্ত পাত আঁতৰাওক",
    "Improve drainage / পানী নিষ্কাশন ব্যৱস্থা উন্নত কৰক"
],

"healthy": [
    "Maintain regular irrigation / নিয়মিত পানী যোগান বজাই ৰাখক",
    "Balanced NPK application / সমতুলিত NPK সাৰ প্ৰয়োগ কৰক",
    "Periodic monitoring / সময় সময়ত পৰ্যবেক্ষণ কৰক"
],

"red rust": [
    "Spray Abamectin 1.9% EC at 1 ml/litre / এবামেক্টিন ১.৯% EC প্ৰতি লিটাৰত ১ মি.লি. স্প্ৰে কৰক",
    "Maintain proper shade / যথাযথ ছাঁ বজাই ৰাখক",
    "Avoid water stress / পানীৰ অভাৱ এৰাই চলক"
]
}


# =====================================================
# 5. MAIN PREDICTION
# =====================================================

def predict_quality(img_path):

    try:
        # ----- Image Preprocess -----
        img = image.load_img(img_path, target_size=(224,224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # ----- Model Predict -----
        preds = model.predict(img_array)[0]

        class_index = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)

        # SAFE MAPPING
        disease = CLASS_ORDER[class_index]
        severity = get_severity(confidence)

        treatment = TREATMENT_GUIDE.get(
            disease,
            ["Consult local agriculture officer"]
        )

        ai_result = {
            "disease": disease,
            "severity": severity,
            "confidence": round(confidence, 2),
            "treatment": treatment
        }

        # =================================================
        # 6. HIT + FUSION (SAFE WRAPPER)
        # =================================================

        try:
            hit_result = hit_rules(img_path)
            final = fuse_decision(ai_result, hit_result)
            return final

        except Exception as hit_error:
            print("⚠ HIT/FUSION FAILED:", hit_error)

            # Fallback to pure AI
            return ai_result


    except Exception as e:
        print("❌ PREDICTION ERROR:", e)

        return {
            "error": "1",
            "message": str(e)
        }
