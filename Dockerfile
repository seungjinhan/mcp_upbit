FROM python:3.11-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY server.py .

# 실행 권한 부여
RUN chmod +x server.py

# 서버 실행
CMD ["python", "server.py"]