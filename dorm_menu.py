import requests
from bs4 import BeautifulSoup
import os

base = "https://dorm.inha.ac.kr"
url = "https://dorm.inha.ac.kr/dorm/10136/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZG9ybSUyRjI1MzMlMkZhcnRjbExpc3QuZG8lM0Y%3D"
response = requests.get(url)

if response.status_code == 200:
    # 요청 성공
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one('table.artclTable')
    titles = table.select('tbody > tr> td._artclTdTitle > a')
    recent = table.a.attrs['href']

    #최신 급식표 보드 접속
    rurl = base + recent
    recent_page = requests.get(rurl)
    board = recent_page.text
    soups = BeautifulSoup(board, 'html.parser')
    files = soups.select_one('body > div > div.artclItem.viewForm > dl > dd > ul > li > a')
    filelink = files.attrs['href']
    filename =  files.text.strip()

    # 다운로드 파일 다운로드
    downlink = base + filelink
    file = requests.get(downlink)
    f = open(filename, 'wb')
    for chunk in file.iter_content(100000):
        f.write(chunk)
    f.close()
    
    #파일 실행
    os.startfile(filename)
else :
    print(response.status_code)

