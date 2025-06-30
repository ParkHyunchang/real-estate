import requests

# 네이버 부동산에서 복사한 실제 헤더를 아래에 입력하세요.
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NTEyNzI1MTksImV4cCI6MTc1MTI4MzMxOX0.WIbbbxvnGHXJ5sLlm26NsQbOj9ilZKmkAu-pggQTW68',
    'cookie': 'REALESTATE=Mon%20Jun%2030%202025%2017%3A35%3A19%20GMT%2B0900%20(Korean%20Standard%20Time); PROP_TEST_KEY=1751272519295.a9faec968b6dff42d99f183074aae9bd777296927703c3c8ea8ee452e088a2eb; PROP_TEST_ID=58275db28510d8b3a5e868951bc67148a786ed1a91963c851f69f846fe7658bd; NAC=2KteCQhejqCdD; _fwb=204peHvtsO1kfzzRBhCsOc9.1751272521787; SRT30=1751272525; NNB=FKD6YFKNJRRGQ; SRT5=1751273629; BUC=iiDbpYf3ndpjYAc7BIpflIYYxd42gGLK6Q01pl2sXe0=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'referer' : 'https://new.land.naver.com/complexes/396?ms=37.4935426,126.9119716,16&a=APT:ABYG:JGC:PRE&e=RETAIL&articleNo=2535057781'
}

def fetch_article_detail(article_no, headers):
    url = f"https://new.land.naver.com/api/articles/{article_no}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    print("[DEBUG] 원본 응답:", data)  # 원본 응답 전체 출력
    detail = data.get("articleDetail", {})
    addition = data.get("articleAddition", {})
    return {
        "동": detail.get("buildingName"),
        "층": addition.get("floorInfo"),
        "가격": addition.get("dealOrWarrantPrc"),
        "면적": addition.get("areaName"),
        "타입": detail.get("tradeTypeName"),
        "articleNo": detail.get("articleNo"),
    }

if __name__ == "__main__":
    print("[네이버 부동산 articleNo로 매물 상세 정보 조회]")
    article_no = input("articleNo(매물번호)를 입력하세요: ").strip()
    if not article_no:
        print("articleNo를 입력해야 합니다.")
    else:
        try:
            detail = fetch_article_detail(article_no, headers)
            print("\n[매물 상세 정보]")
            for k, v in detail.items():
                print(f"{k}: {v}")
        except Exception as e:
            print("매물 정보를 가져오는 데 실패했습니다:", e) 