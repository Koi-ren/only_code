import requests
from bs4 import BeautifulSoup

# 1. URL 요청
url = "https://comic.naver.com/index" # 네이버웹툰
response = requests.get(url)

soup = BeautifulSoup(response.text,  'html.parser')
body = soup.body
title = body.find_all("li.AsideList__item--i30ly span.ContentTitle__title--e3qXt")

# 결과물 리스트 선언
result = []

for i in range(len(title)):
    result.append({'순위': i + 1, '제목': title[i].text, '작가': author[i].text})
    if i == 4: break
        
for name in result:
    print(f'{name['순위']}. {name['제목']} - {name['작가']}')