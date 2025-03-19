import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver

def get_realtime_best():
    # url 설정
    url = "https://comic.naver.com/index"
    # 셀레니움 드라이버 설정
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # 페이지 소스 추출
    soup = bs(driver.page_source, 'html.parser')
    body = soup.body
    title = body.select("li.AsideList__item--i30ly span.ContentTitle__title--e3qXt")
    author = body.select("li.AsideList__item--i30ly a.ContentAuthor__author--CTAAP")

    # 결과물 리스트 선언
    result = []

    for i in range(len(title)):
        result.append({'순위': i + 1, '제목': title[i].text, '작가': author[i].text})
        if i == 4: break

    print('실시간 인기웹툰 순위입니다!')
    print('='*30)
    for name in result:
        print(f'{name['순위']}. {name['제목']} - {name['작가']}')

    driver.quit()

def main():
    get_realtime_best()

if __name__ =='__main__':
    main()