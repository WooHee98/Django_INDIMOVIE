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

        # 광주독립영화관 상영예정작 크롤링 DB삽입(완성)
        ##개봉일 정보가 없는 영화는 가져오지 않았음.

        import requests
        from bs4 import BeautifulSoup
        import urllib
        from selenium import webdriver
        import time
        import re
        import pymysql

        con = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb', charset='utf8')

        cursor = con.cursor()
        statement = "INSERT INTO MOVIE(m_title, m_title_id, m_genre, m_runtime, m_opendate, m_class, m_class_id,  m_director, m_actor, m_scenario, m_image_url) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        select = "SELECT * FROM MOVIE WHERE m_title_id =%s"

        driver = webdriver.PhantomJS("user/lib/phantomjs")
        driver.get("http://gift4u.or.kr/bbs/board.php?bo_table=a02")

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        details = soup.find_all("span", {"class": "typeA"})
        for detail in details:
            a = detail.find("a")
            url = a["href"]
            res = requests.get(url)
            html = res.text
            soup = BeautifulSoup(html, "html.parser")

            movie_view = soup.find("div", {"class": "pt"})

            title = movie_view.find("h5").text.strip()

            title_id = title.replace(" ", "").replace(":", "").strip()
            cursor.execute(select, (title_id,))
            # select_length: select쿼리문 실행했을때 실행한 결과들 가져올때마다 1씩올린다.
            select_length = 0
            for _ in cursor:
                select_length += 1
            # select_length가 0보다 크다면 있는것
            if select_length > 0:
                continue

            if "(" not in title:
                lis = movie_view.find_all("li")[0:8]

            if lis[1].find("strong").text == "출연 : ":
                director = lis[0].contents[1]
                actor = lis[1].contents[1]
                agelimit = lis[2].contents[1]
                age_id = agelimit.strip().replace(" ", "").replace("세", "").replace("관람가", "").replace("이상", "")
                genre = lis[3].contents[1]
                runtime = lis[6].contents[1]

                schedule_box = soup.find("div", {"class": "ico_box"})
                openschedule = schedule_box.find("pre").text.split("*")[0].replace(" ", "").strip()
                # 요일 정보까지 나오는 개봉일 정보라면
                if "(" in openschedule:
                    openschedule = openschedule.split("(")[0]

                thumb_url = soup.find("div", {"id": "bo_v_img"}).find("img")["src"]
                urllib.request.urlretrieve(thumb_url,
                                           "///" + "/mysite/static/img/movie/" + title_id.replace(
                                               ":", "-").replace("\t", "").replace("<", "[").replace(">",
                                                                                                     "]") + "_poster.jpg")

                scenario = soup.find("div", {"class": "opt mt_30 mb_20"}).text.strip()

                print(title)
                print(director)
                print(actor)
                print(agelimit)
                print(runtime)
                print(genre)
                print(openschedule)
                print(scenario)
                print("===============================================")
                print()
                cursor.execute(statement, (title, title_id, genre, runtime, openschedule, agelimit, age_id, director, actor, scenario,
                title_id.replace(":", "-").replace("\t", "").replace("<", "[").replace(">", "]") + "_poster.jpg"))

        con.commit()
        con.close()
        print("finish")
