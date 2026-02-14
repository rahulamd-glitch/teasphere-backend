from fastapi import APIRouter

router = APIRouter()

# In-memory DB (perfect for hackathon)
batch_db = {}

@router.get("/batch/{batch_id}")
def get_batch(batch_id: str):
    return batch_db.get(batch_id, {"error": "Batch not found"})
