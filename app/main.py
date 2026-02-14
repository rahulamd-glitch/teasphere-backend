from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routes import predict, batch

app = FastAPI(title="TeaSphere AI Engine")

# ✅ CORS (CRITICAL for frontend on other laptop)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Static files for QR images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ API routes
app.include_router(predict.router, prefix="/api")
app.include_router(batch.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "TeaSphere backend running"}


