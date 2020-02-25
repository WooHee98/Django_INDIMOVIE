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

        # 아리랑시네센터 상영예정작 DB저장

        import requests
        from bs4 import BeautifulSoup
        import urllib
        from selenium import webdriver
        import time
        import re
        import pymysql

        con = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb', charset='utf8')

        driver = webdriver.PhantomJS("user/lib/phantomjs")
        driver.get("https://cine.arirang.go.kr:8443/arirang/movie/sche.do")

        cursor = con.cursor()
        statement = "INSERT INTO MOVIE(m_title, m_title_id, m_genre, m_runtime, m_opendate, m_class, m_director, m_actor, m_scenario, m_image_url) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        select = "SELECT * FROM MOVIE WHERE m_title_id =%s"

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        null = ""
        details = soup.find_all("a", {"title": "영화정보"})

        for detail in details:
            url = "https://cine.arirang.go.kr:8443/arirang/movie/sche.do" + detail['href']
            res = requests.get(url)
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            movie_view = soup.find("div", {"class": "running-detail-box movie-detail-box"})
            title = movie_view.find("span", {"class": "detail-movie-title"}).text.split("(")[0].strip()

            title_id = title.replace(" ", "").replace(":", "").strip()

            cursor.execute(select, (title_id,))
            # select_length: select쿼리문 실행했을때 실행한 결과들 가져올때마다 1씩올린다.
            select_length = 0
            for _ in cursor:
                select_length += 1
            # select_length가 0보다 크다면 있는것
            if select_length > 0:
                continue

            dl = movie_view.find_all("dl")[0:7]
            direc = dl[0].contents[2].text
            actor = dl[1].contents[2].text.strip()
            genre = dl[3].contents[2].text
            age = dl[4].contents[3].text.strip()
            runtime = dl[5].contents[2].text
            opendate = dl[6].contents[2].text.replace("-", "/").replace(" ", "").strip()
            scenario = soup.find("p", {"class": "con-p"}).text.strip()
            poster_url = "https://cine.arirang.go.kr:8443" + movie_view.find("div", {"class": "left-box"}).find("img")[
                "src"]

            urllib.request.urlretrieve(poster_url,
                                       "///" + "/mysite/static/img/movie/" + title_id + "_poster.jpg")
            print(title)
            print(direc)
            print(actor)
            print(genre)
            print(age)
            print(runtime)
            print(opendate)
            print(scenario)
            print("=========================================================")

            cursor.execute(statement, (
            title, title_id, genre, runtime, opendate, age, direc, actor, scenario, title_id + "_poster.jpg"))

        con.commit()
        con.close()
        print("finish")

