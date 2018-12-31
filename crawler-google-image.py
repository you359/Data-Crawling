"""
네이버 이미지 검색 및 일괄 다운로드
"""
import urllib
import requests
from tqdm import tqdm   #프로그레스 바 표시를 위한 라이브러리
import os

from bs4 import BeautifulSoup
from PIL import Image


def save_image_to_file(image, dirname, suffix):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

    im = Image.open(image.raw)
    im.save('{dirname}/{suffix}.{format}'.format(dirname=dirname, suffix=suffix, format=im.format))

keyword = "불"
encoded_keyword = urllib.parse.quote(keyword)

# HTTP Error 403: Forbidden
# bot user에 대한 server security 에 의해 발생할 수 있음! (구글 이미지 검색의 경우)
# 해결 : 해더 정보 전달
URL = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=" + encoded_keyword
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()

soup = BeautifulSoup(html, 'html.parser')

img_list = []
for i in soup.findAll("img", attrs={'class':'_img'}):
    img_data = {}
    # 이미지 설명, url, 높이, 너비를 dict 형태로 구성
    img_data['alt'] = i['alt']
    img_data['data_source'] = i['data-source']
    img_data['height'] = i['data-height']
    img_data['width'] = i['data-width']

    # 이미지 정보를 담은 dict를 리스트에 추가
    img_list.append(img_data)

for index, img_data in tqdm(enumerate(img_list)):
    # 이미지 URL에서 데이터 파일 가져오기
    response = requests.get(img_data['data_source'], stream=True, timeout=2)
    # 이미지 데이터 파일 저장하기
    save_image_to_file(response, keyword, index)
