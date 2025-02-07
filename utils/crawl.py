from selenium import webdriver
import time
from bs4 import BeautifulSoup

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