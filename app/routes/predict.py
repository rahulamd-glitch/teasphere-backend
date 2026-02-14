from fastapi import APIRouter, UploadFile, File
from PIL import Image
import uuid
import os

from app.ai.model import predict_quality
from app.utils.qr import generate_qr
from app.routes.batch import batch_db

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    batch_id = f"{uuid.uuid4()}.jpg"
    path = os.path.join(UPLOAD_DIR, batch_id)

    try:
        # 🔥 Force RGB conversion
        image = Image.open(file.file).convert("RGB")
        image.save(path, format="JPEG")

        # ✅ Pass FULL PATH
        prediction = predict_quality(path)

        qr_path = generate_qr(batch_id)

        batch_db[batch_id] = {
            "batch_id": batch_id,
            "analysis": prediction,
            "qr_code": qr_path
        }

        return batch_db[batch_id]

    except Exception as e:
        return {
            "error": "1",
            "message": str(e)
        }
