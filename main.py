from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import os

app = FastAPI()

# Docker 클라이언트 초기화
client = docker.from_env()

# 요청으로 받을 데이터 모델 정의
class RunScriptRequest(BaseModel):
    script_name: str

# 지정한 Python 파일을 Docker에서 실행
@app.post("/run-docker-script")
def run_docker_script(request: RunScriptRequest):
    script_name = request.script_name

    # 실행할 스크립트 경로 설정
    script_path = f"./{script_name}"

    # 스크립트가 존재하는지 확인
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Script not found")
    
    try:
        # Docker 이미지를 빌드
        build_response = client.images.build(
            path="./docker",  # Dockerfile이 있는 경로
            tag="my-python-app",  # 빌드할 이미지의 태그
            rm=True  # 빌드 후 중간 컨테이너 제거
        )

        # Docker 컨테이너에서 해당 스크립트를 실행
        container = client.containers.run(
            "my-python-app",  # 빌드한 Docker 이미지 이름
            f"python {script_path}",  # 실행할 스크립트 명령어
            detach=True
        )

        # 컨테이너 실행 결과 로그 가져오기
        logs = container.logs()
        return {"status": "success", "logs": logs.decode("utf-8")}

    except docker.errors.ContainerError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except docker.errors.ImageNotFound as e:
        raise HTTPException(status_code=500, detail="Docker 이미지가 없습니다.")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail="Docker API 오류 발생")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
