import time
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def card_links_fetch(URL):
    '''해당 URL(랭킹 차트)의 카드 URL을 저장'''

    # Chrome WebDriver 실행
    driver = webdriver.Chrome()
    
    # 지정된 URL 접속
    driver.get(URL)

    # 페이지가 로드될 시간을 확보 (5초 대기)
    time.sleep(5)

    # 페이지의 HTML 소스 가져오기
    html_source = driver.page_source

    # WebDriver 종료 (브라우저 닫기)
    driver.quit()

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_source, 'html.parser')

    # 카드 랭킹 리스트에서 각 카드의 상세 페이지 링크 추출
    # 'ul.rk_lst div.card_img a' 선택자를 사용하여 <a> 태그에서 'href' 속성을 가져옴
    # 각 링크 앞에 'https://www.card-gorilla.com' 도메인을 추가하여 전체 URL을 생성
    card_links = ['https://www.card-gorilla.com' + str(link.get('href')) for link in soup.select('ul.rk_lst div.card_img a')]

    # 카드 개수 및 URL 리스트 출력
    print(f'카드의 개수 : {len(card_links)}')
    
    # 카드 링크 리스트 반환
    return card_links


def card_info_fetch(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    # 페이지가 로드될 시간을 확보 (5초 대기)
    time.sleep(5)

    # 페이지의 HTML 소스 가져오기
    html_source = driver.page_source

    # 페이지 닫기
    driver.quit()

    # HTML 형식으로 파싱
    soup = BeautifulSoup(html_source, 'html.parser')

    # 카드 이미지를 저장할 경로
    save_folder = 'card_image/check_card'

    img_tag = soup.select_one('div.card_img img')

    if img_tag:
        img_url = img_tag.get('src')  # src 속성 가져오기
        
        # 절대 URL로 변환
        if img_url and img_url.startswith('http'):
            img_full_url = img_url
        else:
            img_full_url = URL + img_url if img_url else None
        
        if img_full_url:
            try:
                # 이미지 다운로드
                img_data = requests.get(img_full_url).content
                img_name = os.path.join(save_folder, img_url.split('/')[-1])  # 이미지 이름 설정

                # 이미지 파일 저장
                with open(img_name, 'wb') as f:
                    f.write(img_data)
                print(f"Downloaded: {img_name}")
            except Exception as e:
                print(f"Failed to download {img_full_url}: {e}")

    # 카드 내용 상세히 크롤링
    title = soup.select_one('title').text[8:].strip() # 카드 이름
    benefit_summary = soup.find('meta', attrs={'name': 'description'}).get('content') # 혜택 요약
    text = soup.find('div', attrs={'class':'el-popover'}).get_text(separator=' ', strip=True)
    annual_fee = text[9:] # 연회비 상세안내

    bene_total = [bene.select_one('p').text for bene in soup.select('article.cmd_con dt')] # 혜택 이름(모음)
    bene_content = [bene.find("i", attrs={"data-v-b3ba76c4": True}).get_text() for bene in soup.select('article.cmd_con dt')] # 주요혜택 카테고리별 요약
    # bene_detail = [bene.text for bene in soup.select('article.cmd_con div.in_box')] # 주요혜택 카테고리별 디테일


    # 딕셔너리 생성
    result = {}
    result[title] = {}
    result[title]['혜택 요약'] = benefit_summary
    result[title]['연회비 상세안내'] = annual_fee
    result[title]['주요 혜택'] = {}
    result[title]['카드 이미지'] = img_name

    for i in range(len(bene_total)):
        result[title]['주요 혜택'][bene_total[i]] = bene_content[i]

    return result