# 네이버 부동산 매물 정보 수집기

네이버 부동산에서 매물 정보를 수집하고 엑셀/CSV 파일로 정리하는 프로그램입니다.

## 🐍 Python 3.11 설치 및 가상환경(venv) 사용법

### 1. Python 3.11 설치

1. [Python 3.11 다운로드 페이지](https://www.python.org/downloads/release/python-3110/)로 이동
2. Windows용 설치 파일 다운로드 및 실행
3. **설치 시 "Add Python to PATH" 꼭 체크**
4. 설치 완료 후, 명령 프롬프트(cmd)에서 아래 명령어로 버전 확인
   ```bash
   python --version
   # 또는
   py --version
   ```
   → `Python 3.11.x`가 나오면 정상

### 2. 가상환경(venv) 만들기 및 활성화

**가상환경은 프로젝트별로 독립적인 Python 환경을 만들어줍니다.**

1. 프로젝트 폴더로 이동
   ```bash
   cd C:\Users\hyunc\personal_project\real-estate
   ```
2. 가상환경 생성 (venv311이라는 이름으로)
   ```bash
   py -3.11 -m venv venv311
   ```
3. 가상환경 활성화 (Windows PowerShell)
   ```powershell
   .\venv311\Scripts\Activate.ps1
   ```
   (cmd에서는 `venv311\Scripts\activate.bat`)
4. 가상환경이 활성화되면 프롬프트에 `(venv311)`이 표시됨
5. 가상환경에서 Python 버전 확인
   ```bash
   python --version
   # → Python 3.11.x
   ```
6. 패키지 설치 및 실행은 반드시 가상환경이 활성화된 상태에서 진행

### 3. 패키지 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚡️ check_complex_deals.py 사용법 (메인 실행 파일)

1. 가상환경이 활성화된 상태에서 아래 명령어 실행
   ```bash
   python check_complex_deals.py
   ```
2. 단지번호와 면적코드를 입력하면 매매/전세/월세별 매물 정보를 확인할 수 있습니다.

> **참고:** 이 프로젝트의 메인 실행 파일은 `check_complex_deals.py`입니다. 기존의 `main.py`는 더 이상 사용하지 않습니다.

## 기타 안내

- 여러 Python 버전이 설치되어 있다면, 항상 3.11 가상환경을 사용하세요.
- 가상환경을 끄려면 `deactivate` 명령어 입력
- 쿠키/Authorization 등은 네이버 정책에 따라 주기적으로 갱신 필요
- 본 프로젝트는 교육/개인용이며, 네이버 정책을 반드시 준수하세요.

## 기능

- ✅ 매물 정보 수집 (현재: 샘플 데이터)
- ✅ 데이터 정리 및 분류
- ✅ 통계 정보 생성
- ✅ 엑셀/CSV 파일로 내보내기
- ✅ 필터링 및 정렬 기능

## 설치 및 실행

### 1. Python 설치
Python 3.8 이상을 설치하세요:
- [Python 공식 사이트](https://www.python.org/downloads/)
- 설치 시 "Add Python to PATH" 옵션을 체크하세요

### 2. 프로젝트 설정
```bash
# 프로젝트 폴더로 이동
cd real-estate

# 가상환경 생성 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 3. 프로그램 실행

#### 간단한 테스트 (권장)
```bash
python simple_test.py
```

## 사용법

### 1. 네이버 부동산 네트워크에서 real?complexNO=1234&areaNO=1  -> 이거 있는거 찾아서 우클릭 - copy - copy as curl 눌러서 해당 데이터 확인해서 check_complex_deals.py 여기 코드에 알맞게 수정
```bash
 # 실제 네이버 부동산에서 복사한 헤더 (쿠키, Authorization 등)
    headers = {
        ~~
    }
```

### 참고
```
check_complex_deals -> 실제 매물
check_landprice_deals -> 모든 매매가
```

## 출력 파일

프로그램 실행 후 `output/` 폴더에 다음 파일들이 생성됩니다:

- `real_estate_data_YYYYMMDD_HHMMSS.csv` - CSV 형식
- `test_sample_YYYYMMDD_HHMMSS.xlsx` - 엑셀 형식 (테스트용)
- `{지역}_{매물유형}_{거래유형}_{타임스탬프}.xlsx` - 엑셀 형식 (메인)

## 엑셀 파일 구성

생성된 엑셀 파일은 다음 시트들을 포함합니다:

1. **매물정보** - 수집된 매물 데이터
2. **통계정보** - 가격, 면적, 지역별 통계
3. **필터가이드** - 엑셀 필터링 방법 안내

## 문제 해결

### Python이 인식되지 않는 경우
1. Python이 제대로 설치되었는지 확인
2. 환경 변수 PATH에 Python이 추가되었는지 확인
3. 터미널/명령 프롬프트를 재시작

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 개별 패키지 설치
pip install pandas
pip install openpyxl
pip install requests
pip install beautifulsoup4
```

### 권한 오류
- 관리자 권한으로 터미널 실행
- 가상환경 사용 권장

## 향후 계획

- [ ] 실제 네이버 부동산 웹 스크래핑 구현
- [ ] 더 많은 지역 및 매물 유형 지원
- [ ] 실시간 가격 변동 추적
- [ ] 웹 인터페이스 추가
- [ ] 데이터베이스 연동

## 주의사항

- 네이버 부동산의 이용약관을 준수하여 사용하세요
- 과도한 요청은 피해주세요
- 수집된 데이터는 개인적인 용도로만 사용하세요
- 상업적 용도로 사용하지 마세요

## 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로만 제공됩니다. 