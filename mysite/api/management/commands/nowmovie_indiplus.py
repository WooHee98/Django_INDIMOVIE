from django.core.management.base import BaseCommand, CommandError

import requests
from bs4 import BeautifulSoup
import urllib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from time import sleep

from datetime import datetime

class Command(BaseCommand):
    help = '헬프 명령어에 표시될 내용'

    def add_arguments(self, parser):
        # optional param 직접 플래그를 입력해야 값이 들어가는 param
        parser.add_argument('--date', nargs=1)

        # # positional param 위치를 바탕으로 입력해야하는 param
        # parser.add_argument('bar0', nargs=1)
        # parser.add_argument('bar1', nargs=1)
        # parser.add_argument('bar2', nargs=1)
        pass

    def handle(self, *args, **options):
        print("실행됨")

        # 인디플러스천안 현재상영작 DB저장

        import requests
        from bs4 import BeautifulSoup
        import urllib
        from selenium import webdriver
        import time
        import re
        import pymysql

        con = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8')

        driver = webdriver.Chrome("C:\workspace/chromedriver.exe")
        driver.get("http://xn--2z1bz7ch1njvc5tdy9k60p.kr/information/movie.php?mtype=Y")

        cursor = con.cursor()
        statement = "INSERT INTO MOVIE(m_title, m_title_id, m_genre, m_runtime, m_opendate, m_class, m_class_id,m_director, m_actor, m_scenario, m_image_url) VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
        select = "SELECT * FROM MOVIE WHERE m_title_id =%s"

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        detailss = soup.find("td", {"class": "con_line2"})
        dd = detailss.find_all("td", {"class": "vtop"})

        for detail in dd:
            a = detail.find("a")
            url = "http://xn--2z1bz7ch1njvc5tdy9k60p.kr/information/" + a["href"]
            res = requests.get(url)
            # 한글 꺠짐현상
            res.encoding = 'cp949'
            html = res.text
            soup = BeautifulSoup(html, "html.parser")

            movie_view = soup.find("td", {"class": "con_line2 BP30"})

            movie_view1 = movie_view.find_all("td", {"class": "vtop"})
            lid = movie_view1[1]
            lis = lid.find_all("td")[0:7]

            title = lis[0].text.strip().replace(":감독판", "").strip()

            title_id = title.replace(" ", "").strip()

            cursor.execute(select, (title_id))
            # select_length: select쿼리문 실행했을때 실행한 결과들 가져올때마다 1씩올린다.
            select_length = 0
            for _ in cursor:
                select_length += 1
            # select_length가 0보다 크다면 있는것
            if select_length > 0:
                continue

            direc = lis[1].text.strip()
            actor = lis[2].contents[1].strip()
            age = lis[3].contents[1].strip()
            age_id = age.strip().replace(" ", "").replace("세", "").replace("관람가", "").replace("이상", "")
            genre = lis[4].contents[1].strip()
            runtime = lis[5].contents[1].strip()
            opendate1 = lis[6].contents[1].strip()
            opendate = opendate1.replace("년", "/").replace("월", "/").replace("일", "").replace(" ", "")

            poster_url = " http://xn--2z1bz7ch1njvc5tdy9k60p.kr" + movie_view.find("img")["src"]
            urllib.request.urlretrieve(poster_url,
                                       "C:/Users/eunju/indimovie8/mysite/static/img/movie/" + title_id.replace(":",
                                                                                                                   "") + "_poster.jpg")

            print(poster_url)
            print(title)
            print(direc)
            print(actor)
            print(age)
            print(age_id)
            print(genre)
            print(runtime)
            print(opendate)
            movie_content = soup.find("td", {"class": "TP10 BP10"})

            if movie_content.find("p") in movie_content:
                content1 = movie_content.find("p").text
                if movie_content.find("h5") in movie_content:
                    content = movie_content.find("h5").text
                    scenario = content + content1
                    scenario = scenario.encode("euc-kr", "ignore").decode("euc-kr")
                    print(scenario)
                else:
                    scenario = content1
                    scenario = scenario.encode("euc-kr", "ignore").decode("euc-kr")
                    print(scenario)
            else:
                print()

            print("========================================================")
            print()
            cursor.execute(statement, (title, title_id, genre, runtime, opendate, age, age_id, direc, actor, scenario,
                                       title_id.replace(":", "") + "_poster.jpg"))

        con.commit()
        con.close()
        print("finish")



