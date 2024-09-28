# 베이스 이미지로 Python 사용
FROM python:3.9-slim

# 컨테이너 내에서 작업할 디렉토리 설정
WORKDIR /usr/src/app

# 모든 Python 파일 복사
COPY *.py ./

# 필요한 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# CMD는 기본적으로 아무것도 실행하지 않도록 설정
CMD ["tail", "-f", "/dev/null"]