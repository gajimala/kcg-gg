# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# firebase 서비스 계정 복사
COPY firebase-service-account.json ./

# 종속성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사 (public 폴더 포함)
COPY . .
COPY public/ ./public/

# 환경변수 PORT 기본값 설정 (클라우드런에서 자동 설정해 줌)
ENV PORT 8080
EXPOSE 8080

# FastAPI 실행 - 포트를 환경변수 PORT로 동적으로 지정
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
