"""
네이버 쇼핑-GPU 검색의 각 상품 이름과 가격 크롤링하기
"""
import urllib
from bs4 import BeautifulSoup

# 가져올 웹 페이지 URL
URL = "https://search.shopping.naver.com/search/all.nhn?where=all&frm=NVSCTAB&query=gpu"

# request 객체 생성
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})

# 설정한 url의 html code 내용 읽어오기
html = urllib.request.urlopen(req).read()
# html = urllib.request.urlopen(url).read() 도 가능!!

# html 문서의 파싱 가능한 BeautifulSoup 객체 생성
soup = BeautifulSoup(html, 'html.parser')

# <ul class="goods_list"></ul>로 감싸진 영역 가져오기!
ul = soup.find("ul", class_="goods_list")

products_list = []
# <li class="_itemSection"></li>로 감싸진 영역 가져오기!
for li in ul.findAll("li", class_="_itemSection"):
    product = {}

    # <a class="tit"></a>로 감싸진 영역 가져오기!
    product["name"] = li.find("a", class_="tit").get_text().strip()

    # <span class="price"></span>로 감싸진 영역 가져오기!
    product["price"] = li.find("span", class_="price").get_text().strip()
    products_list.append(product)

# 출력해보기!
print(products_list)