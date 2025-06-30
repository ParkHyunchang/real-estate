import requests

def get_trade_type_name(trade_type):
    return {"A1": "매매", "B1": "전세", "B2": "월세"}.get(trade_type, trade_type)

def fetch_complex_deals(complex_no, area_no):
    trade_types = ["A1", "B1", "B2"]  # 매매, 전세, 월세
    results = {}

    # 실제 네이버 부동산에서 복사한 헤더 (쿠키, Authorization 등)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NTEyNTQwNDcsImV4cCI6MTc1MTI2NDg0N30.rlZIouT3yhC-58FVCSec6sfH_Ii2fA4Sz-tafGZymQ8",
        "Cookie": "NNB=WVGDSAP2LYDWQ; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; landHomeFlashUseYn=Y; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; NAC=Av9GBowM63VI; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nid_inf=1702075088; NID_AUT=i2Ok3bDQz8SYCHnMWG4vggKS8cv97BkEbBcCaurnImREHcPCE03E2OYHR+rh7J4Y; REALESTATE=Mon%20Jun%2030%202025%2012%3A27%3A27%20GMT%2B0900%20(Korean%20Standard%20Time); PROP_TEST_KEY=1751254047184.bf1dcddbc13be7517b278b9632e5896d2bed4c895dd19f1e61980b4fd8469c10; PROP_TEST_ID=2efed223be17099b09a1309693e8a8490fb954bb1a46429f2c962756ed3b6c1f; SRT30=1751257228; NID_SES=AAABqCu2vBVhH++hqOxImowQ3ICUxR4d1dM5VWkrRudlJDOvxQje3PKzmsli1nlUAtP0PO1G1rTDoJDHnD2te24bScByMiHzelU5geaToy7M7hCINTNBfZ3473DVxOHeumDyIobyFp9bT+O1r8uB2CD5rq2Yi/cW84J7M4aQnBdDnU5Sa75+QQbscauja1FnBiCplE6lpykVNM4DPi9dFfj4IJbgyTQXSsv3aSxpiD/hkuwDMn3GqPO4EoPIqKZV6U0x2twG2wXOBgDC0yHaUBjvFlrvtT1xetrk+RBgbj3GDtpb5JeRgDIQFkWSIlHgs1wbtEXG4DaLw5NfYIKGHh2ChzOkxR1FRKU2z0QtC3PAOdJk0ZMGHqY9HrOrcAXoYhAqh3c2hl0VCQAzJg8LYco1P4YtBPEqtoSjKVaNVvk2GgTdGAKQUmuUDbPMzwG00bQbx0FSLkcfILUsCO2l4onsyg0mh1EUA8/jgRk7IPVH0FBtHVQht1w7kLJkXDkevuhtrmMaQytAvto7ozWXD4DRV1zX5KuvO8ZPDnxEVlAF5UJbpRQuI/M42rTv4fkWVcmpdQ==; SRT5=1751268425; BUC=Nev_6BUPJHJjgNYWmfvkZVD_yZg55k_uOnM1_Av1NEw=",
        "Referer": "https://new.land.naver.com/complexes/3386?ms=37.494631,126.9142735,17&a=APT:ABYG:JGC:PRE&e=RETAIL&articleNo=2534835130",
    }

    for trade_type in trade_types:
        url = (
            f"https://new.land.naver.com/api/complexes/{complex_no}/prices/real"
            f"?complexNo={complex_no}&tradeType={trade_type}&areaNo={area_no}&type=table"
        )
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[DEBUG] {trade_type} 원본 응답:", data)  # 원본 응답 출력
            real_price_on_month_list = data.get("realPriceOnMonthList", [])
            print(f"[DEBUG] {trade_type} real_price_on_month_list:", real_price_on_month_list)  # 월별 리스트 출력
            ho_list = []
            for month in real_price_on_month_list:
                real_price_list = month.get("realPriceList", [])
                for deal in real_price_list:
                    date = f"{deal.get('tradeYear', '')}.{deal.get('tradeMonth', '')}.{deal.get('tradeDate', '')}"
                    floor = deal.get("floor", "")
                    price = deal.get("formattedPrice", "")
                    ho_list.append(f"{date} | {floor}층 | {price}")
            print(f"[DEBUG] {trade_type} ho_list:", ho_list)  # 최종 결과 리스트 출력
            results[trade_type] = ho_list
        else:
            results[trade_type] = None  # 요청 실패

    return results

if __name__ == "__main__":
    complex_no = input("단지번호를 입력하세요 (예: 3386): ").strip()
    area_no = input("면적코드(areaNo)를 입력하세요 (보통 1~5, 모르면 1): ").strip() or "1"

    results = fetch_complex_deals(complex_no, area_no)
    for trade_type, ho_list in results.items():
        print(f"\n[{get_trade_type_name(trade_type)}]")
        if ho_list is None:
            print("  ❌ 요청 실패")
        elif ho_list:
            print(f"  매물 {len(ho_list)}건")
            for ho in ho_list:
                print("   -", ho)
        else:
            print("  매물이 없습니다.") 