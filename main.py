from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os
import firebase_admin
from firebase_admin import credentials, db

app = FastAPI()

# CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "firebase-service-account.json")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL", "https://kcghelp-default-rtdb.firebaseio.com")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})

class HelpRequest(BaseModel):
    lat: float
    lng: float
    timestamp: float

@app.post("/requests")
def request_help(data: HelpRequest):
    ref = db.reference('requests')
    ref.push(data.dict())
    return {"status": "ok"}

@app.get("/requests")
def get_requests():
    ref = db.reference('requests')
    snapshot = ref.get()
    return snapshot if snapshot else {}

# public 폴더에 있는 정적파일 서빙
app.mount("/", StaticFiles(directory="public", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
