import qrcode
import os

BASE_URL = "http://10.186.201.31:8000"

def generate_qr(batch_id):
    # QR should point to batch details, not image file
    qr_link = f"{BASE_URL}/api/batch/{batch_id}"

    qr_path = f"uploads/{batch_id}_qr.png"

    img = qrcode.make(qr_link)
    img.save(qr_path)

    return qr_link   # 🔥 RETURN LINK, NOT FILE PATH
