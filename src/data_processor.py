#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

class DataProcessor:
    """데이터 처리 및 정리 클래스"""
    
    def __init__(self):
        self.processed_data = []
    
    def process_properties(self, properties):
        """매물 데이터 처리"""
        try:
            processed_properties = []
            
            for property_data in properties:
                if property_data:
                    processed_property = self._process_single_property(property_data)
                    if processed_property:
                        processed_properties.append(processed_property)
            
            self.processed_data = processed_properties
            return processed_properties
            
        except Exception as e:
            print(f"데이터 처리 중 오류 발생: {str(e)}")
            return []
    
    def _process_single_property(self, property_data):
        """단일 매물 데이터 처리"""
        try:
            processed = property_data.copy()
            
            # 가격 정보 정리
            if '가격' in processed:
                processed['가격'] = self._clean_price(processed['가격'])
            
            # 면적 정보 정리
            if '면적' in processed:
                processed['면적'] = self._clean_area(processed['면적'])
            
            # 층수 정보 정리
            if '층수' in processed:
                processed['층수'] = self._clean_floor(processed['층수'])
            
            # 방향 정보 정리
            if '방향' in processed:
                processed['방향'] = self._clean_direction(processed['방향'])
            
            # 주소 정보 정리
            if '주소' in processed:
                processed['주소'] = self._clean_address(processed['주소'])
            
            # 추가 정보 생성
            processed = self._add_derived_info(processed)
            
            return processed
            
        except Exception as e:
            print(f"단일 매물 처리 중 오류: {str(e)}")
            return None
    
    def _clean_price(self, price):
        """가격 정보 정리"""
        try:
            if isinstance(price, (int, float)):
                return price
            
            if isinstance(price, str):
                # 숫자만 추출
                numbers = re.findall(r'\d+', price.replace(',', ''))
                if numbers:
                    return int(numbers[0])
            
            return 0
        except:
            return 0
    
    def _clean_area(self, area):
        """면적 정보 정리"""
        try:
            if isinstance(area, (int, float)):
                return float(area)
            
            if isinstance(area, str):
                # 숫자만 추출 (소수점 포함)
                numbers = re.findall(r'\d+\.?\d*', area)
                if numbers:
                    return float(numbers[0])
            
            return 0
        except:
            return 0
    
    def _clean_floor(self, floor):
        """층수 정보 정리"""
        try:
            if isinstance(floor, str):
                # 숫자만 추출
                numbers = re.findall(r'\d+', floor)
                if numbers:
                    return f"{numbers[0]}층"
                return floor
            return floor
        except:
            return "정보 없음"
    
    def _clean_direction(self, direction):
        """방향 정보 정리"""
        try:
            if isinstance(direction, str):
                # 방향 정보 정리
                direction = direction.strip()
                if not direction or direction == "":
                    return "정보 없음"
                return direction
            return "정보 없음"
        except:
            return "정보 없음"
    
    def _clean_address(self, address):
        """주소 정보 정리"""
        try:
            if isinstance(address, str):
                address = address.strip()
                if not address or address == "":
                    return "정보 없음"
                return address
            return "정보 없음"
        except:
            return "정보 없음"
    
    def _add_derived_info(self, property_data):
        """추가 정보 생성"""
        try:
            # 가격대 분류
            if '가격' in property_data and property_data['가격'] > 0:
                price = property_data['가격']
                if price < 5000:
                    property_data['가격대'] = "5천만원 미만"
                elif price < 10000:
                    property_data['가격대'] = "5천만원~1억원"
                elif price < 20000:
                    property_data['가격대'] = "1억원~2억원"
                elif price < 50000:
                    property_data['가격대'] = "2억원~5억원"
                else:
                    property_data['가격대'] = "5억원 이상"
            else:
                property_data['가격대'] = "정보 없음"
            
            # 면적대 분류
            if '면적' in property_data and property_data['면적'] > 0:
                area = property_data['면적']
                if area < 20:
                    property_data['면적대'] = "20㎡ 미만"
                elif area < 30:
                    property_data['면적대'] = "20~30㎡"
                elif area < 50:
                    property_data['면적대'] = "30~50㎡"
                elif area < 80:
                    property_data['면적대'] = "50~80㎡"
                else:
                    property_data['면적대'] = "80㎡ 이상"
            else:
                property_data['면적대'] = "정보 없음"
            
            # 지역 정보 추출
            if '주소' in property_data:
                address = property_data['주소']
                if isinstance(address, str):
                    # 시/도 추출
                    city_match = re.search(r'([가-힣]+시|[가-힣]+도)', address)
                    if city_match:
                        property_data['시도'] = city_match.group(1)
                    else:
                        property_data['시도'] = "정보 없음"
                    
                    # 구/군 추출
                    district_match = re.search(r'([가-힣]+구|[가-힣]+군)', address)
                    if district_match:
                        property_data['구군'] = district_match.group(1)
                    else:
                        property_data['구군'] = "정보 없음"
                else:
                    property_data['시도'] = "정보 없음"
                    property_data['구군'] = "정보 없음"
            
            # 매물 유형 추출
            if '매물명' in property_data:
                name = property_data['매물명']
                if isinstance(name, str):
                    if '아파트' in name or 'APT' in name.upper():
                        property_data['매물유형'] = "아파트"
                    elif '빌라' in name or 'VL' in name.upper():
                        property_data['매물유형'] = "빌라"
                    elif '원룸' in name or 'OR' in name.upper():
                        property_data['매물유형'] = "원룸"
                    elif '오피스텔' in name or 'OP' in name.upper():
                        property_data['매물유형'] = "오피스텔"
                    else:
                        property_data['매물유형'] = "기타"
                else:
                    property_data['매물유형'] = "정보 없음"
            
            return property_data
            
        except Exception as e:
            print(f"추가 정보 생성 중 오류: {str(e)}")
            return property_data
    
    def filter_properties(self, filters=None):
        """매물 필터링"""
        try:
            if not filters:
                return self.processed_data
            
            filtered_data = []
            
            for property_data in self.processed_data:
                if self._matches_filters(property_data, filters):
                    filtered_data.append(property_data)
            
            return filtered_data
            
        except Exception as e:
            print(f"필터링 중 오류 발생: {str(e)}")
            return []
    
    def _matches_filters(self, property_data, filters):
        """필터 조건 확인"""
        try:
            for filter_key, filter_value in filters.items():
                if filter_key in property_data:
                    property_value = property_data[filter_key]
                    
                    # 숫자 비교
                    if isinstance(filter_value, (int, float)) and isinstance(property_value, (int, float)):
                        if filter_key.startswith('min_'):
                            if property_value < filter_value:
                                return False
                        elif filter_key.startswith('max_'):
                            if property_value > filter_value:
                                return False
                        else:
                            if property_value != filter_value:
                                return False
                    
                    # 문자열 비교
                    elif isinstance(filter_value, str) and isinstance(property_value, str):
                        if filter_value.lower() not in property_value.lower():
                            return False
            
            return True
            
        except Exception as e:
            print(f"필터 조건 확인 중 오류: {str(e)}")
            return False
    
    def sort_properties(self, sort_by='가격', ascending=True):
        """매물 정렬"""
        try:
            if not self.processed_data:
                return []
            
            # 정렬 가능한 필드 확인
            if sort_by not in self.processed_data[0]:
                print(f"⚠️ 정렬 필드 '{sort_by}'를 찾을 수 없습니다.")
                return self.processed_data
            
            # 정렬
            sorted_data = sorted(
                self.processed_data,
                key=lambda x: x.get(sort_by, 0) if isinstance(x.get(sort_by), (int, float)) else str(x.get(sort_by, '')),
                reverse=not ascending
            )
            
            return sorted_data
            
        except Exception as e:
            print(f"정렬 중 오류 발생: {str(e)}")
            return self.processed_data
    
    def get_statistics(self):
        """통계 정보 생성"""
        try:
            if not self.processed_data:
                return {}
            
            stats = {
                '총_매물수': len(self.processed_data),
                '가격_통계': {},
                '면적_통계': {},
                '지역_분포': {},
                '매물유형_분포': {}
            }
            
            # 가격 통계
            prices = [p.get('가격', 0) for p in self.processed_data if p.get('가격', 0) > 0]
            if prices:
                stats['가격_통계'] = {
                    '평균': sum(prices) / len(prices),
                    '최소': min(prices),
                    '최대': max(prices),
                    '중간값': sorted(prices)[len(prices)//2]
                }
            
            # 면적 통계
            areas = [p.get('면적', 0) for p in self.processed_data if p.get('면적', 0) > 0]
            if areas:
                stats['면적_통계'] = {
                    '평균': sum(areas) / len(areas),
                    '최소': min(areas),
                    '최대': max(areas),
                    '중간값': sorted(areas)[len(areas)//2]
                }
            
            # 지역 분포
            regions = {}
            for p in self.processed_data:
                region = p.get('구군', '정보 없음')
                regions[region] = regions.get(region, 0) + 1
            stats['지역_분포'] = regions
            
            # 매물 유형 분포
            types = {}
            for p in self.processed_data:
                prop_type = p.get('매물유형', '정보 없음')
                types[prop_type] = types.get(prop_type, 0) + 1
            stats['매물유형_분포'] = types
            
            return stats
            
        except Exception as e:
            print(f"통계 생성 중 오류 발생: {str(e)}")
            return {}
    
    def remove_duplicates(self):
        """중복 매물 제거"""
        try:
            if not self.processed_data:
                return []
            
            seen = set()
            unique_properties = []
            
            for property_data in self.processed_data:
                # 매물명과 주소로 중복 판단
                key = f"{property_data.get('매물명', '')}_{property_data.get('주소', '')}"
                
                if key not in seen:
                    seen.add(key)
                    unique_properties.append(property_data)
            
            removed_count = len(self.processed_data) - len(unique_properties)
            if removed_count > 0:
                print(f"✅ 중복 매물 {removed_count}개를 제거했습니다.")
            
            self.processed_data = unique_properties
            return unique_properties
            
        except Exception as e:
            print(f"중복 제거 중 오류 발생: {str(e)}")
            return self.processed_data 