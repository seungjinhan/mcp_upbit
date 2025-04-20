FROM python:3.11-alpine

# 시스템 종속성 설치
RUN apk add --no-cache gcc musl-dev linux-headers

# 작업 디렉토리 설정
WORKDIR /app

# 모든 파일 복사
COPY . /app

# Python 종속성 설치
RUN pip install --upgrade pip \
    && pip install --no-cache-dir .

# MCP 서버 실행
CMD ["python", "-m", "mcp_upbit.server"]