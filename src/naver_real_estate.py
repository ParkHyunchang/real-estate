#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json

class NaverRealEstateAPI:
    """네이버 부동산 웹 스크래핑 클래스"""
    
    def __init__(self):
        self.base_url = "https://new.land.naver.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
    
    def search_properties(self, region, property_type, trade_type, page=1):
        """매물 검색 - 실제 네이버 부동산 스크래핑"""
        print(f"🔍 {region} {property_type} {trade_type} 매물 검색 중... (페이지 {page})")
        
        try:
            # 네이버 부동산 검색 URL 구성
            search_url = self._build_search_url(region, property_type, trade_type, page)
            print(f"📡 URL: {search_url}")
            
            # 웹페이지 요청
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 매물 정보 추출
            properties = self._extract_properties_from_page(soup, region, property_type, trade_type)
            
            print(f"✅ {len(properties)}개의 매물을 찾았습니다.")
            
            # 요청 간격 조절 (서버 부하 방지)
            time.sleep(random.uniform(2, 4))
            
            return properties
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 네트워크 오류: {str(e)}")
            print("⚠️ 샘플 데이터를 반환합니다.")
            return self._generate_sample_data(region, property_type, trade_type, page)
        except Exception as e:
            print(f"❌ 스크래핑 오류: {str(e)}")
            print("⚠️ 샘플 데이터를 반환합니다.")
            return self._generate_sample_data(region, property_type, trade_type, page)
    
    def _build_search_url(self, region, property_type, trade_type, page):
        """검색 URL 구성"""
        # 네이버 부동산 검색 URL 패턴
        base_url = "https://new.land.naver.com/complexes"
        
        # 지역 코드 매핑
        region_mapping = {
            '서울': '1100000000',
            '부산': '2100000000',
            '대구': '2200000000',
            '인천': '2300000000',
            '광주': '2400000000',
            '대전': '2500000000',
            '울산': '2600000000',
            '세종': '4100000000',
            '경기': '3100000000',
            '강원': '3200000000',
            '충북': '3300000000',
            '충남': '3400000000',
            '전북': '3500000000',
            '전남': '3600000000',
            '경북': '3700000000',
            '경남': '3800000000',
            '제주': '3900000000',
        }
        
        # 매물 유형 매핑
        property_mapping = {
            '아파트': 'APT',
            '빌라': 'VL',
            '원룸': 'OR',
            '오피스텔': 'OP',
            '단독주택': 'DD',
            '상가': 'SG'
        }
        
        # 거래 유형 매핑
        trade_mapping = {
            '매매': 'A1',
            '전세': 'B1',
            '월세': 'B2'
        }
        
        region_code = region_mapping.get(region, '1100000000')
        property_code = property_mapping.get(property_type, 'APT')
        trade_code = trade_mapping.get(trade_type, 'A1')
        
        return f"{base_url}?ms={region_code}&a={property_code}&b={trade_code}&page={page}"
    
    def _extract_properties_from_page(self, soup, region, property_type, trade_type):
        """페이지에서 매물 정보 추출"""
        properties = []
        
        try:
            # 네이버 부동산의 실제 HTML 구조에 맞춰 선택자 수정
            # 매물 목록 컨테이너 찾기
            property_containers = soup.find_all('div', class_=re.compile(r'item|property|complex'))
            
            if not property_containers:
                # 다른 선택자 시도
                property_containers = soup.find_all('a', href=re.compile(r'/complexes/'))
            
            if not property_containers:
                # JSON 데이터에서 추출 시도
                properties = self._extract_from_json_data(soup)
                if properties:
                    return properties
            
            # HTML에서 매물 정보 추출
            for container in property_containers[:20]:  # 최대 20개
                try:
                    property_info = self._extract_single_property(container, region, property_type, trade_type)
                    if property_info:
                        properties.append(property_info)
                except Exception as e:
                    print(f"매물 정보 추출 중 오류: {str(e)}")
                    continue
            
            # 매물이 없으면 JSON 데이터에서 추출 시도
            if not properties:
                properties = self._extract_from_json_data(soup)
            
        except Exception as e:
            print(f"페이지 파싱 중 오류: {str(e)}")
        
        return properties
    
    def _extract_from_json_data(self, soup):
        """JSON 데이터에서 매물 정보 추출"""
        properties = []
        
        try:
            # 페이지 내 JSON 데이터 찾기
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'window.__NEXT_DATA__' in script.string:
                    # JSON 데이터 파싱
                    json_text = script.string.split('window.__NEXT_DATA__ = ')[1].split(';</script>')[0]
                    data = json.loads(json_text)
                    
                    # 매물 정보 추출
                    properties = self._parse_json_properties(data)
                    break
                    
        except Exception as e:
            print(f"JSON 데이터 파싱 중 오류: {str(e)}")
        
        return properties
    
    def _parse_json_properties(self, data):
        """JSON 데이터에서 매물 정보 파싱"""
        properties = []
        
        try:
            # 네이버 부동산 JSON 구조에 맞춰 파싱
            # 실제 구조는 네이버 부동산 사이트 분석 필요
            
            # 예시 구조 (실제로는 사이트 분석 후 수정 필요)
            if 'props' in data and 'pageProps' in data['props']:
                page_props = data['props']['pageProps']
                
                # 매물 목록 찾기
                if 'complexList' in page_props:
                    complex_list = page_props['complexList']
                    
                    for complex_item in complex_list:
                        property_info = {
                            '매물명': complex_item.get('complexName', '정보 없음'),
                            '가격': self._extract_price_from_json(complex_item),
                            '가격표시': complex_item.get('priceDisplay', '정보 없음'),
                            '면적': complex_item.get('area', 0),
                            '면적표시': f"{complex_item.get('area', 0)}㎡",
                            '층수': f"{complex_item.get('floor', 0)}층",
                            '방향': complex_item.get('direction', '정보 없음'),
                            '주소': complex_item.get('address', '정보 없음'),
                            'URL': f"https://new.land.naver.com/complexes/{complex_item.get('complexNo', '')}",
                            '수집시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        properties.append(property_info)
            
        except Exception as e:
            print(f"JSON 파싱 중 오류: {str(e)}")
        
        return properties
    
    def _extract_single_property(self, container, region, property_type, trade_type):
        """단일 매물 정보 추출"""
        try:
            property_info = {}
            
            # 매물명 추출
            name_element = container.find(['h3', 'h4', 'div'], class_=re.compile(r'title|name'))
            if name_element:
                property_info['매물명'] = name_element.get_text(strip=True)
            else:
                property_info['매물명'] = f"{region} {property_type}"
            
            # 가격 정보 추출
            price_element = container.find(['span', 'div'], class_=re.compile(r'price|cost'))
            if price_element:
                price_text = price_element.get_text(strip=True)
                property_info['가격'] = self._extract_price(price_text)
                property_info['가격표시'] = price_text
            else:
                property_info['가격'] = 0
                property_info['가격표시'] = "정보 없음"
            
            # 면적 정보 추출
            area_element = container.find(['span', 'div'], class_=re.compile(r'area|size'))
            if area_element:
                area_text = area_element.get_text(strip=True)
                property_info['면적'] = self._extract_area(area_text)
                property_info['면적표시'] = area_text
            else:
                property_info['면적'] = 0
                property_info['면적표시'] = "정보 없음"
            
            # 층수 정보 추출
            floor_element = container.find(['span', 'div'], class_=re.compile(r'floor|level'))
            if floor_element:
                property_info['층수'] = floor_element.get_text(strip=True)
            else:
                property_info['층수'] = "정보 없음"
            
            # 방향 정보 추출
            direction_element = container.find(['span', 'div'], class_=re.compile(r'direction|orientation'))
            if direction_element:
                property_info['방향'] = direction_element.get_text(strip=True)
            else:
                property_info['방향'] = "정보 없음"
            
            # 주소 정보 추출
            address_element = container.find(['span', 'div'], class_=re.compile(r'address|location'))
            if address_element:
                property_info['주소'] = address_element.get_text(strip=True)
            else:
                property_info['주소'] = f"{region} 지역"
            
            # URL 정보 추출
            if container.name == 'a' and container.get('href'):
                property_info['URL'] = self.base_url + container['href']
            else:
                property_info['URL'] = ""
            
            # 수집 시간
            property_info['수집시간'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return property_info
            
        except Exception as e:
            print(f"단일 매물 추출 중 오류: {str(e)}")
            return None
    
    def _extract_price_from_json(self, item):
        """JSON에서 가격 추출"""
        try:
            price = item.get('price', 0)
            if isinstance(price, str):
                return self._extract_price(price)
            return price
        except:
            return 0
    
    def _extract_price(self, price_text):
        """가격 정보에서 숫자 추출"""
        try:
            # 숫자만 추출
            numbers = re.findall(r'\d+', price_text.replace(',', ''))
            if numbers:
                return int(numbers[0])
            return 0
        except:
            return 0
    
    def _extract_area(self, area_text):
        """면적 정보에서 숫자 추출"""
        try:
            # 숫자만 추출 (소수점 포함)
            numbers = re.findall(r'\d+\.?\d*', area_text)
            if numbers:
                return float(numbers[0])
            return 0
        except:
            return 0
    
    def _generate_sample_data(self, region, property_type, trade_type, page):
        """샘플 매물 데이터 생성 (백업용)"""
        sample_properties = []
        
        # 페이지별로 다른 데이터 생성
        base_count = (page - 1) * 10
        
        for i in range(10):
            property_id = base_count + i + 1
            
            # 가격 범위 설정
            if property_type == "아파트":
                price_range = (8000, 50000)
                area_range = (25, 120)
            elif property_type == "빌라":
                price_range = (5000, 25000)
                area_range = (20, 80)
            elif property_type == "원룸":
                price_range = (3000, 15000)
                area_range = (15, 40)
            else:  # 오피스텔
                price_range = (6000, 30000)
                area_range = (20, 60)
            
            # 랜덤 값 생성
            price = random.randint(price_range[0], price_range[1]) * 1000
            area = round(random.uniform(area_range[0], area_range[1]), 1)
            floor = random.randint(1, 25)
            
            # 방향 설정
            directions = ["남향", "북향", "동향", "서향", "남동향", "남서향", "북동향", "북서향"]
            direction = random.choice(directions)
            
            # 지역별 주소 생성
            addresses = {
                "서울": [
                    "서울특별시 강남구 강남대로",
                    "서울특별시 마포구 홍대로", 
                    "서울특별시 송파구 올림픽로",
                    "서울특별시 서초구 서초대로",
                    "서울특별시 종로구 종로"
                ],
                "부산": [
                    "부산광역시 해운대구 해운대로",
                    "부산광역시 부산진구 중앙대로",
                    "부산광역시 동래구 중앙대로",
                    "부산광역시 남구 용당로"
                ],
                "대구": [
                    "대구광역시 중구 동성로",
                    "대구광역시 수성구 동대구로",
                    "대구광역시 북구 칠성로"
                ]
            }
            
            region_addresses = addresses.get(region, addresses["서울"])
            base_address = random.choice(region_addresses)
            address_number = random.randint(100, 999)
            
            property_info = {
                '매물명': f"{region} {property_type} {property_id}호",
                '가격': price,
                '가격표시': f"{price//10000}억 {price%10000//1000}천만원" if price >= 10000 else f"{price//1000}천만원",
                '면적': area,
                '면적표시': f"{area}㎡",
                '층수': f"{floor}층",
                '방향': direction,
                '주소': f"{base_address} {address_number}",
                'URL': f"https://new.land.naver.com/properties/{property_id}",
                '수집시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            sample_properties.append(property_info)
        
        return sample_properties
    
    def get_property_detail(self, property_url):
        """매물 상세 정보 조회"""
        try:
            response = self.session.get(property_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 상세 정보 추출
            detail_info = {}
            
            # 기본 정보 추출
            detail_info['상세주소'] = self._extract_text(soup, '.address, [class*="address"]')
            detail_info['건물정보'] = self._extract_text(soup, '.building_info, [class*="building"]')
            detail_info['입주가능일'] = self._extract_text(soup, '.move_in_date, [class*="move"]')
            detail_info['주차'] = self._extract_text(soup, '.parking, [class*="parking"]')
            detail_info['엘리베이터'] = self._extract_text(soup, '.elevator, [class*="elevator"]')
            detail_info['난방'] = self._extract_text(soup, '.heating, [class*="heating"]')
            
            return detail_info
            
        except Exception as e:
            print(f"상세 정보 조회 중 오류: {str(e)}")
            return {}
    
    def _extract_text(self, soup, selector):
        """BeautifulSoup에서 텍스트 추출"""
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else ""
        except:
            return "" 