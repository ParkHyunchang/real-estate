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
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NTEyNDQ4NDMsImV4cCI6MTc1MTI1NTY0M30.6GVmuEB-vvJbu5TMsxWa-fZZyFx7NZN-ZCux57mxG34",
        "Cookie": "NNB=WVGDSAP2LYDWQ; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; landHomeFlashUseYn=Y; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; NAC=Av9GBowM63VI; NACT=1; SRT30=1751243108; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nid_inf=1702075088; NID_AUT=i2Ok3bDQz8SYCHnMWG4vggKS8cv97BkEbBcCaurnImREHcPCE03E2OYHR+rh7J4Y; REALESTATE=Mon%20Jun%2030%202025%2009%3A54%3A03%20GMT%2B0900%20(Korean%20Standard%20Time); PROP_TEST_KEY=1751244843908.c00e3c93a5c45df2e8f40c1c380f72574fd6fe833ff55aee7334a0756b6aef1a; PROP_TEST_ID=ca6e2b8f82e48fc285925e0854f25e7bc27ea0e9ac17a71f1d3b183fc8585f58; NID_SES=AAABqsacywUBBP2Jm2/wJtmxrnaX25misermG0Q4SA5mwScf3ZlePon5n2ySbhx945NASd5U4nxp34d6vXjyV/NREwa6Cpg2qLOmo/tejTImF+Hea/taX1mhNHxL/oXyezc7QIcjGtIFwpxDI1O4UN5wVxFp1+1xu9J5GIkPoj6fdzGcf71e3QNda1cycexdBuiqeqF6OPy/ROtWJiKNsbz/SYo/o1YhgoojSkgsUC91+mlrsvUgMNqt8KvBElvchTHZi6Fs5JaX6+x0oyRPpsZNOZZ10p2SXPxSzsslz8I6RqneKdnh4p+mUD6ixG7aQxs/Of+0cdBGBu4YdUeWJD1VmIkNcaN3CODDl3WBnrKNPovpGrWZ3CmQB0X6xrStQwEIB/sW+0HEtCG8FTW7wu4fWeCsFfyOGSW1I8ixNCYZcODTRRZ4HSTsXwkHI7YopNs3ysDP0JEHB3GS/QYFyH6mSNSNhsjNHWClIRqmmAL8gnDDTkVyOuv1n00394xY0m6s9ifRYffZgLCHoF6vvl3La6D669g2rLyEqXnMr5QEe8bNZow2g9fdZiuAll7dIjqMUg==; SRT5=1751251266; BUC=44VviKooNcT2w4Wg1GZIpU1MuX0r1SChE67i8eRx3Es=",
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
            real_price_on_month_list = data.get("realPriceOnMonthList", [])
            ho_list = []
            for month in real_price_on_month_list:
                real_price_list = month.get("realPriceList", [])
                for deal in real_price_list:
                    date = f"{deal.get('tradeYear', '')}.{deal.get('tradeMonth', '')}.{deal.get('tradeDate', '')}"
                    floor = deal.get("floor", "")
                    price = deal.get("formattedPrice", "")
                    ho_list.append(f"{date} | {floor}층 | {price}")
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