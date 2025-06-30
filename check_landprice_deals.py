import requests

# 네이버 부동산에서 복사한 실제 헤더를 아래에 입력했습니다.
headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NTEyNDQ4NDMsImV4cCI6MTc1MTI1NTY0M30.6GVmuEB-vvJbu5TMsxWa-fZZyFx7NZN-ZCux57mxG34',
    'cookie': 'NNB=WVGDSAP2LYDWQ; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; landHomeFlashUseYn=Y; _fwb=123m7KSkEOCkRR3Nrcqt3Vo.1746600589639; NAC=Av9GBowM63VI; NACT=1; SRT30=1751243108; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nid_inf=1702075088; NID_AUT=i2Ok3bDQz8SYCHnMWG4vggKS8cv97BkEbBcCaurnImREHcPCE03E2OYHR+rh7J4Y; REALESTATE=Mon%20Jun%2030%202025%2009%3A54%3A03%20GMT%2B0900%20(Korean%20Standard%20Time); PROP_TEST_KEY=1751244843908.c00e3c93a5c45df2e8f40c1c380f72574fd6fe833ff55aee7334a0756b6aef1a; PROP_TEST_ID=ca6e2b8f82e48fc285925e0854f25e7bc27ea0e9ac17a71f1d3b183fc8585f58; NID_SES=AAABqqFZBQN4wKQQKLBviz4vJrTUvbzUbMCVPc4BaTJfM/aoH6oOlrrjtED1wBtFWwZMYjvuceMxis6aR4I2/6iTU3bsVhgtC3AWXvE2PSP1jOyMSiuGt+vm5/h4/+eUinAhMoScV3GhK2cFhP4blYPyySXcxM6Gl/iVbUv11b/o9UcNdpam+EIwTI2CGbACTLZvPuoIA1oE2JWK56DLdVqx0Fjh3C8R2WavRoKkERysyVfsl99BmN//2iQgx6+9F/RB4Z35QnNXkRxigWD/xK3oB6Vh6mxSZzTQ0fErPaNQiGVpJVeXo9igZ0daquPwe8GMEBQpKOBuU0qrvso40xdXHouEQQhTRlw6rvhftpz/rBHml2saKFVdjGETJR3XSwe+oFpwND/jj4EN1MNV5ykcVwp73jVie2SNzyERtUcnRMyhNkmLbgk5cUt8qUybElAESo+OJjdKvqCUEGuLRS8bDyLlWjvxz3cSK62lGTgqP0bFVWVjO7gQZj9pmUtYLILs1MW3IFQ4XrohYdDCp/gLRicjpk0aDy06LTZS4PHwTmAXrgjlWGp8dxWHeQedee4Q1A==; SRT5=1751252469; BUC=_yiMPYBsZt6Vc9kex7jmOyNx6oB8WN1NhPFFsaoQu8Q=',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes/3386?ms=37.494631,126.9142735,17&a=APT:ABYG:JGC:PRE&e=RETAIL&articleNo=2534854287',
    'sec-ch-ua': 'Google Chrome;v=137, Chromium;v=137, Not/A)Brand;v=24',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

def format_price_kr(price):
    try:
        price = int(price)
    except:
        return price
    if price >= 10000_0000:
        return f"{price // 10000_0000}억 {((price % 10000_0000) // 10000):,}만 원" if (price % 10000_0000) else f"{price // 10000_0000}억 원"
    elif price >= 10000:
        return f"{price // 10000}만 원"
    else:
        return f"{price:,}원"

def get_landprice_deals(complex_no, dong_no):
    url = f"https://new.land.naver.com/api/complexes/{complex_no}/buildings/landprice?dongNo={dong_no}&complexNo={complex_no}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print("[DEBUG] 원본 응답 데이터:", data)  # 원본 응답 전체 출력
    results = []
    floors = data.get("landPriceTotal", {}).get("landPriceFloors", [])
    print("[DEBUG] floors:", floors)  # 파싱된 층 정보 리스트 출력
    for floor_info in floors:
        floor = floor_info.get("floor")
        for price_info in floor_info.get("landPrices", []):
            dong = price_info.get("dongNm")
            ho = price_info.get("hoNm")
            price = price_info.get("price")
            ptp_no = price_info.get("ptpNo")
            if ptp_no == "1":
                deal_type = "전세"
            elif ptp_no == "2":
                deal_type = "월세"
            elif ptp_no == "3":
                deal_type = "매매"
            else:
                deal_type = "-"
            results.append({
                "동": dong,
                "호": ho,
                "층": floor,
                "가격": price,
                "거래유형": deal_type
            })
    print("[DEBUG] results:", results)  # 최종 결과 리스트 출력
    return results

if __name__ == "__main__":
    print("[네이버 부동산 landprice API 동/호/층/가격 조회]")
    # 기본값 예시: complex_no=3386, dong_no=864373
    complex_no = input("단지번호(complexNo)를 입력하세요 [기본값: 3386]: ").strip() or "3386"
    dong_no = input("동번호(dongNo)를 입력하세요 [기본값: 864373]: ").strip() or "864373"
    deals = get_landprice_deals(complex_no, dong_no)
    if not deals:
        print("매물 정보가 없습니다.")
    else:
        for deal in deals:
            price_str = format_price_kr(deal['가격'])
            print(f"{deal['동']}동 {deal['호']}호 {deal['층']}층 [{deal['거래유형']}]: {price_str}") 