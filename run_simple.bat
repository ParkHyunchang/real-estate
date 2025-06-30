@echo off
echo 🏠 네이버 부동산 매물 수집기 - 간단 테스트
echo ================================================

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치해주세요.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 설치 확인 완료

REM 간단한 테스트 실행
echo 🚀 간단한 테스트를 시작합니다...
python simple_test.py

if errorlevel 1 (
    echo ❌ 테스트 실행 중 오류가 발생했습니다.
    echo Python과 필요한 패키지가 설치되어 있는지 확인해주세요.
) else (
    echo ✅ 테스트가 성공적으로 완료되었습니다.
    echo 📁 output 폴더에서 결과 파일을 확인하세요.
)

echo.
echo 프로그램이 종료되었습니다.
pause 