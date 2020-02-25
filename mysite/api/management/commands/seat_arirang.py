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

        # 아리랑시네센터 맥스무비 크롤링 디비저장 완성

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

        import pymysql
        import os
        import re
        import shutil

        def selectQuery(q, *data):
            conn = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb', charset='utf8',
                                   use_unicode=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(q, data)
            rows = curs.fetchall()
            conn.close()
            return [{k: str(v) for k, v in row.items()} for row in rows]

        def insertQuery(q, *data):
            conn = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb', charset='utf8',
                                   use_unicode=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(q, data)
            lastId = curs.lastrowid
            conn.commit()
            conn.close()
            return lastId

        def insertQueryWithoutId(q, *data):
            conn = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb', charset='utf8',
                                   use_unicode=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(q, data)
            conn.commit()
            conn.close()

        driver = webdriver.PhantomJS("user/lib/phantomjs")

        # 기본설정
        userId = "kerri981230"
        userPwd = "leewoohee1525!"

        # 로그인 폼 찾기
        driver.get("http://www.maxmovie.com/")
        driver.implicitly_wait(5)

        nav = driver.find_element_by_id("MySub")
        login_menu = nav.find_element_by_tag_name("*")
        login_menu.click()

        # id & pwd 입력
        id_input = driver.find_element_by_id("uid")
        pwd_input = driver.find_element_by_id("upw")
        id_input.send_keys(userId)
        pwd_input.send_keys(userPwd)

        # 로그인 버튼 클릭
        sleep(3)
        # driver.execute_script("$('p.logbt > a').click();")
        # driver.implicitly_wait(20)
        btn_login = driver.find_element_by_css_selector("p.logbt").find_element_by_tag_name('a')

        # driver.implicitly_wait(20)
        btn_login.send_keys(Keys.ENTER)
        driver.implicitly_wait(20)
        sleep(3)

        # 영화예매 탭이 로드될때까지 기다리게 하기
        try:
            element = WebDriverWait(driver, 10).until(

                cond.presence_of_element_located((By.ID, "GnbTop2"))
            )
        finally:
            driver.implicitly_wait(5)
            driver.get("https://ticket.maxmovie.com/reserve/movie")

        # '극장먼저선택' 클릭
        pre_theater = driver.find_element_by_css_selector("li[class='rn2']")
        btn_theater = pre_theater.find_element_by_tag_name("*")
        btn_theater.click()

        driver.implicitly_wait(10)

        # 영화관 검색 후 클릭
        search_theater = driver.find_element_by_id("txtQuickSearch")
        theaterName = "아리랑시네센터"
        search_theater.send_keys(theaterName)

        # 상위디렉토리 생성
        os.mkdir("///" + "/" + theaterName + "/")

        find_theater = driver.find_element_by_id("ulQuickSearchResult")
        find_theater.find_element_by_tag_name("*").click()

        ## 선가능한 날짜 리스트 선택
        sleep(1)
        # 달력 버튼
        today_box = driver.find_element_by_css_selector("p.tday > a.day")
        sleep(1)
        today_box.click()
        sleep(1)
        today_box.click()

        """
        while 버전
        선택된 날짜를 바탕으로 다음 날짜를 선택하는 것이 가장 이상적임.
        """
        before_day = ""
        cnt = 0
        finished = False
        while not finished:
            # 날짜 선택 박스가 닫혀있다면 그 안에 있는 날짜 클릭이 불가능 => 날짜 선택 박스를 연다
            today_box.click()
            sleep(1)

            # 선택 가능한 날짜 수집
            tt = driver.find_elements_by_css_selector("span.pa")
            sleep(1)
            target = None

            # 선택 가능한 날짜중 다음에 수집해야할 날짜를 선택 before_day가 비어있는경우 첫번째 날짜 수집
            if before_day == "":
                before_day = tt[0].text
                target = tt[0]
            else:
                flag = False
                total = len(tt)
                itr_cnt = 0
                for t in tt:
                    if t.text == before_day:
                        flag = True
                    else:
                        if flag:
                            target = t
                            before_day = t.text
                            break
                        else:
                            if total == itr_cnt:
                                finished = True
                    itr_cnt += 1

            sleep(1)
            # 마지막 날짜까지 수집한 후 target이 None이 됨
            if target is not None and "pc" not in target.get_attribute("class"):
                print(target.text, "일 ================")
                nowdate = datetime.today().strftime("%Y%m")
                now_date = nowdate + target.text
                a_parent = target.find_element_by_xpath("./..")
                sleep(1)
                a_parent.click()
            else:
                print(target.text, "일 ================")
                nowdate = datetime.today().strftime("%Y%m")
                now_date = nowdate + target.text
                today_box.click()
            sleep(2)
            # driver.execute_script("arguments[0].click();", a_parent)

            # 검색 직후 날짜는 초기설정이 되어있음 => 그상태에서 상영정보만 가져오기
            # 그날의 모든 상영스케줄
            if not finished:
                m_list = driver.find_elements_by_css_selector("div.mstimein > ul.mtmlist > li.tmplMovie")
                for m in m_list:
                    # m은 영화 한개를 의미
                    title = m.find_element_by_css_selector("p.pt10 > a")

                    ##title.text ->(띄어쓰기 제거, 특수문자 제거 ...) -> title_id

                    title_id = title.text.strip().replace(" ", "").replace("(디지털)", "").replace("[종영예정]", "").replace(
                        "감독판", "").replace(":", "")
                    print(title_id)
                    select = "SELECT m_id FROM movie WHERE m_title_id=%s"
                    result = selectQuery(select, title_id)

                    ##1) m_id 가 없을때, 스킵하거나 크롤링을 해서 만들어준 후 아래로 진행
                    if len(result) == 0:
                        continue

                    ##2) m_id 가 있다면,
                    m_id = result[0]["m_id"]

                    select = "SELECT t_id FROM TheaterDataDo WHERE t_name=%s"
                    result = selectQuery(select, theaterName)

                    ###1) t_id 가 없을때, 스킵하거나 크롤링을 해서 만들어준 후 아래로 진행
                    if len(result) == 0:
                        continue

                    ###2) t_id 가 있다면,
                    t_id = result[0]["t_id"]

                    # 영화 하나의 상영관에서의 상영스케줄 박스
                    time_schedule = m.find_element_by_css_selector("div[class='gnbox']")
                    if time_schedule.find_elements_by_css_selector("p[class='gntit']"):
                        # 상영스케줄이 여러개라면
                        screens = time_schedule.find_elements_by_css_selector("p[class='gntit']")
                        for screen in screens:
                            screen_id = screen.text.replace("디지털", "").replace("-영문자막", "").replace("디지털-우리말 녹음",
                                                                                                    "").replace(
                                "-우리말 녹음", "")
                            print(screen_id)

                            select = "SELECT st_id FROM ScreenTheater WHERE t_id_id=%s AND st_name=%s"
                            result = selectQuery(select, t_id, screen_id)

                            ####1) st_id 가 없다면, 등록
                            if len(result) == 0:
                                insert = "INSERT into ScreenTheater(st_name, t_id_id) VALUES (%s, %s)"
                                st_id = insertQuery(insert, screen_id, t_id)

                            ####2) st_id 가 있다면,
                            else:
                                st_id = result[0]["st_id"]

                            if time_schedule.find_elements_by_css_selector("ul[class='mti tmplScreen']"):
                                # 해당 영화 하나의 상영스케줄
                                screen_times = time_schedule.find_elements_by_css_selector("ul[class='mti tmplScreen']")
                                for screen_time in screen_times:
                                    # 한 개의 영화의 한 개의 상영관의 상영스케줄
                                    times = screen_time.find_elements_by_tag_name("li")

                                    for time in times:
                                        # 태그를 a로 변경
                                        # try, wait until 구문 추가
                                        start_time = time.find_element_by_tag_name("*")
                                        print(start_time.text.split("종료")[0])

                                        ####상영관 정보 등록
                                        insert = "INSERT into Movietime(m_id_id, st_id_id, mt_day, mt_time) VALUES (%s, %s, %s, %s)"
                                        mt_id = insertQuery(insert, m_id, st_id,
                                                            str(now_date)[:4] + "-" + str(now_date)[4:6] + "-" + str(
                                                                now_date)[6:], start_time.text.split("종료")[0])

                                        # 하위 디렉토리 생
                                        os.makedirs("///\\" + theaterName + "/" + str(mt_id))

                                        # 한 파일 여러 폴더에 동시복사
                                        shutil.copy(
                                            "///\\mysite\\api\\management\\seat\\아리랑시네센터1관.html",
                                            "///" + theaterName + "/" + str(mt_id))
                                        shutil.copy(
                                            "///\\mysite\\api\\management\\seat\\아리랑시네센터2관.html",
                                            "///" + theaterName + "/" + str(mt_id))
                                        shutil.copy(
                                            "///\\mysite\\api\\management\\seat\\아리랑시네센터3관.html",
                                            "///" + theaterName + "/" + str(mt_id))

                                        if "off" in time.get_attribute("class"):
                                            continue
                                        start_time.click()

                                        # 다음단계버튼클릭
                                        btn_next = driver.find_element_by_id("btnGroup0")
                                        btn_next.click()

                                        # 다음페이지 로드까지 기다리기
                                        driver.implicitly_wait(10)

                                        # 개인정보동의버튼 클릭

                                        # 개인정보동의버튼 클릭
                                        driver.implicitly_wait(20)
                                        sleep(3)  # implicitly_wait이 제대로 동작을 하지 않기 때문에 python sleep을 사용하여 3초 딜레이
                                        #################
                                        # find_element 함수가 잘 동작을 안해서 자바스크립트로 해당 버튼 클릭 구현
                                        #################
                                        driver.execute_script("$('h4.spertit').find('a').click();")
                                        driver.implicitly_wait(20)
                                        # btn_check.click()

                                        # 정보수집 동의 후 다음 버튼 클릭
                                        btn_group = driver.find_element_by_id("btnGroup2")
                                        btn_next2 = btn_group.find_elements_by_tag_name("a")[1]
                                        btn_next2.click()

                                        driver.implicitly_wait(20)
                                        sleep(3)  # implicitly_wait이 제대로 동작을 하지 않기 때문에 python sleep을 사용하여 3초 딜레이
                                        #################
                                        # find_element 함수가 잘 동작을 안해서 자바스크립트로 해당 버튼 클릭 구현
                                        #################
                                        driver.execute_script("$('#reserveTicket dd:nth-child(3)').find('a').click();")
                                        driver.implicitly_wait(20)

                                        # 좌석번호 다 가져오기
                                        seat_table = driver.find_element_by_css_selector("div[class='seat_table']")
                                        seats = seat_table.find_elements_by_tag_name("button")
                                        print("좌석리스트—>")
                                        s_no = 1
                                        for seat in seats:
                                            if seat.get_attribute("class"):
                                                # 예매가 완료된 좌석
                                                seat = re.sub('[A-Za-z]', 'alpabet', seat.text)
                                                if 'alpabet' in seat:
                                                    print("pass")
                                                    continue
                                                else:
                                                    s_no += 1
                                            else:
                                                # 예매가 안된 좌석
                                                seat = re.sub('[A-Za-z]', 'alpabet', seat.text)
                                                if 'alpabet' in seat:
                                                    print("pass")
                                                    continue
                                                else:
                                                    s_no += 1

                                            print(s_no, end=' ')
                                            insert = "INSERT INTO seat(s_name, s_reserved, mt_id_id) VALUES(%s, %s, %s)"
                                            insertQueryWithoutId(insert, str(s_no), 0, mt_id)

                                        # 이전으로 돌아가기
                                        print()
                                        btn_group = driver.find_element_by_id("btnGroup2")
                                        btn_before = btn_group.find_elements_by_tag_name("a")[0]
                                        btn_before.click()