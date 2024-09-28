from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Python 코드 요청 모델
class PythonCodeRequest(BaseModel):
    code: str

@app.post("/run-python-code")
def run_python_code(request: PythonCodeRequest):
    code = request.code
    script_path = "/app/temp_script.py"

    with open(script_path, "w") as script_file:
        script_file.write(code)

    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")

# React 코드 요청 모델
class ReactCodeRequest(BaseModel):
    code: str

@app.post("/run-react-code")
def run_react_code(request: ReactCodeRequest):
    code = request.code
    react_path = "/app/react/temp_app.js"

    with open(react_path, "w") as react_file:
        react_file.write(code)

    try:
        # React 앱을 실행하는 명령어
        result = subprocess.run(
            ["npm", "start"],
            cwd="/app/react",  # React 애플리케이션 디렉토리
            capture_output=True,
            text=True
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing React code: {str(e)}")
