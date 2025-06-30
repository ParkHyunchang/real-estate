@echo off
echo 🏠 네이버 부동산 매물 수집기
echo ================================

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 가상환경 확인 및 생성
if not exist "venv" (
    echo 📦 가상환경을 생성합니다...
    python -m venv venv
)

REM 가상환경 활성화
echo 🔧 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM 패키지 설치
echo 📥 필요한 패키지를 설치합니다...
pip install -r requirements.txt

REM 프로그램 실행
echo 🚀 프로그램을 시작합니다...
python main.py

REM 가상환경 비활성화
deactivate

echo.
echo 프로그램이 종료되었습니다.
pause 