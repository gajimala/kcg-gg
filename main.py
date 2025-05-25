import os
import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# Firebase Admin SDK 임포트
import firebase_admin
from firebase_admin import credentials, db

app = FastAPI()

# Firebase 서비스 계정 JSON 파일 경로 (환경변수로 지정하거나 기본값 사용)
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "firebase-service-account.json")

# Firebase Realtime Database URL
# Firebase 콘솔 > Realtime Database > 데이터베이스 URL 복사해서 넣으세요
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL", "https://kcghelp-default-rtdb.firebaseio.com")

# Firebase 앱이 초기화 되어있지 않으면 초기화 수행
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)  # 서비스 계정 키 파일 로드
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL  # 데이터베이스 URL 설정
    })

# 구조 요청 데이터 모델 정의 (lat, lng, timestamp)
class HelpRequest(BaseModel):
    lat: float
    lng: float
    timestamp: float  # 타임스탬프는 ms 단위 예상

# 구조 요청 POST API
@app.post("/requests")
def request_help(data: HelpRequest):
    # Realtime Database 내 'requests' 노드 참조
    ref = db.reference('requests')
    # 새로운 요청을 push 하여 고유키 생성 후 저장
    new_ref = ref.push()
    new_ref.set(data.dict())
    return {"status": "ok"}

# 구조 요청 전체 GET API
@app.get("/requests")
def get_requests():
    ref = db.reference('requests')
    snapshot = ref.get()
    # 데이터가 없으면 빈 딕셔너리 반환
    return snapshot if snapshot else {}

# 정적 파일 서빙 (public 폴더)
app.mount("/", StaticFiles(directory="public", html=True), name="static")
