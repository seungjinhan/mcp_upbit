FROM python:3.11-alpine

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 서버 코드 복사
COPY . .

# 서버 실행
CMD ["python", "server.py"]