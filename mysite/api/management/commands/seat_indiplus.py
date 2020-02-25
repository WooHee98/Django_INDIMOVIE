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

        # 인디플러스천안 좌석 정보 인터파크 크롤링

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

        userId = "ee981215"
        userPwd = "indi1234"
        nowdate = datetime.today().strftime("%Y%m%d")
        now_date = int(nowdate) + 1
        plandate = int(nowdate) + 7

        # 로그인 수행
        # #m_join1 > a
        driver.get("https://movie.interpark.com/Movie/Gate/TPLogin.asp?CPage=M")
        driver.implicitly_wait(5)

        ##loginAllWrap > div.leftLoginBox > iframe
        iframe = driver.find_element_by_css_selector("#loginAllWrap > div.leftLoginBox > iframe")
        driver.switch_to.frame(iframe)

        # id & pwd
        id_input = driver.find_element_by_id("userId")
        pwd_input = driver.find_element_by_id("userPwd")
        id_input.send_keys(userId)
        pwd_input.send_keys(userPwd)

        # 로그인 버튼 클릭
        btn_login = driver.find_element_by_id("btn_login")
        btn_login.click()

        # 로그인 완료 이후 예약 페이지로 이동
        try:
            element = WebDriverWait(driver, 10).until(
                # 영화예매 탭이 로드될때까지 기다리게 하기
                cond.presence_of_element_located((By.ID, "gnbInparkLogo"))
            )
        finally:
            driver.implicitly_wait(5)
            driver.get("https://movie.interpark.com/Movie/2.0/Booking.asp")

        # iframe id값 = frmTheaterSelect
        # 영화관 선택하는 iframe 선택
        driver.implicitly_wait(10)
        iframe = driver.find_element_by_id("frmTheaterSelect")

        driver.switch_to.frame(iframe)
        txtsearch = driver.find_element_by_id("txtTSearch")

        # 영화관 검색
        theaterName = "인디플러스 천안"
        txtsearch.send_keys(theaterName)
        txtsearch.send_keys(Keys.ENTER)

        # 상위 디렉토리 생
        os.mkdir("///" + "/" + theaterName.replace(" ", "") + "/")

        # 영화관 검색 후 결과를 선
        # 인디플러스 천안 id = DV1600052
        theater = driver.find_element_by_id("DV1600052")
        theater.click()

        # 원본 페이지로 이동
        driver.switch_to.default_content()

        # iframe id값 = frmDateSelect
        # 날짜 선택하는 iframe 선택
        iframe = driver.find_element_by_id("frmDateSelect")
        driver.switch_to.frame(iframe)

        # 1주일동안 상영시간표
        while now_date <= plandate:
            # 원본 페이지로 이동
            driver.switch_to.default_content()

            # iframe id값 = frmDateSelect
            # 날짜 선택하는 iframe 선택
            iframe = driver.find_element_by_id("frmDateSelect")
            driver.switch_to.frame(iframe)
            date = driver.find_element_by_id(str(now_date))
            print(now_date)
            tmp = date.find_element_by_tag_name("*")
            tmp.click()
            # 영화 종류별 시간 선택
            driver.switch_to.default_content()

            # iframe id 값 = frmPriceSelect
            # 영화 선택하는 iframe 선택
            iframe = driver.find_element_by_id("frmMovieDateSelect")
            driver.switch_to.frame(iframe)

            tables = driver.find_elements_by_css_selector(
                "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > div > table > tbody > tr > td > table")
            for table in tables:
                ####### 영화별 시간 선택 #########
                # table 은 영화 하나를 의미함.
                # nth-child(2) 사용하면 상영관도 출력 가능

                title = table.find_element_by_css_selector("td:nth-child(1)")

                ##title.text ->(띄어쓰기 제거, 특수문자 제거 ...) -> title_id

                title_id = title.text.strip().replace(" ", "").replace("(디지털)", "").replace("[종영예정]", "").replace(":",
                                                                                                                  "")
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

                screen = table.find_element_by_css_selector("td:nth-child(2)")
                print(screen.text)

                select = "SELECT st_id FROM ScreenTheater WHERE t_id_id=%s AND st_name=%s"
                result = selectQuery(select, t_id, screen.text)

                ####1) st_id 가 없다면, 등록
                if len(result) == 0:
                    insert = "INSERT into ScreenTheater(st_name, t_id_id) VALUES (%s, %s)"
                    st_id = insertQuery(insert, screen.text, t_id)

                ####2) st_id 가 있다면,
                else:
                    st_id = result[0]["st_id"]

                # 영화에 대한 모든 시간 확인
                times = table.find_elements_by_css_selector("table")
                for time in times:
                    if time.text != '':
                        # time은 해당 영화에서 상영회차 하나를 의미함.
                        labels = time.find_elements_by_css_selector("td")
                        for label in labels:
                            # label_text: 상영 시간
                            label_text = label.text

                            if "매진" in label_text:
                                continue
                            else:
                                if label_text.strip() != '':
                                    print(label_text)
                                    link = label.find_element_by_css_selector("a")

                                    ####상영관 정보 등록
                                    insert = "INSERT into movietime(m_id_id, st_id_id, mt_day, mt_time) VALUES (%s, %s, %s, %s)"
                                    mt_id = insertQuery(insert, m_id, st_id,
                                                        str(now_date)[:4] + "-" + str(now_date)[4:6] + "-" + str(
                                                            now_date)[6:], label_text.strip())
                                    # link.click()
                                    # click 함수의 경우 iframe에서 제대로 동작하지 않는 경우 발생

                                    # 하위 디렉토리 생
                                    os.mkdir("///\\" + theaterName.replace(" ", "") + "/" + str(mt_id))

                                    # 한 파일 여러 폴더에 동시복사
                                    shutil.copy("///\\mysite\\api\\management\\seat\\인디플러스천안1관.html",
                                                "///\\" + theaterName.replace(" ", "") + "/" + str(mt_id))

                                    # a 태그에 포함된 자바스크립트를 실행하는 방향으로 진행
                                    link_script = link.get_attribute('href').split(':')[1]

                                    # Selenium을 씀으로써 사용 가능한 메소드 driver.implicitly_wait()
                                    # 브라우저에서 사용되는 엔진 자체에서 파싱되는 시간을 기다린다는 의미
                                    driver.implicitly_wait(10)
                                    driver.execute_script(link_script)
                                    driver.implicitly_wait(5)

                                    # 좌석 확인 페이지로 진행
                                    # frmPriceSelect
                                    driver.switch_to.default_content()
                                    driver.implicitly_wait(20)
                                    iframe2 = driver.find_element_by_id("frmPriceSelect")
                                    driver.implicitly_wait(5)
                                    driver.switch_to.frame(iframe2)
                                    driver.implicitly_wait(20)
                                    # SeatAssign0
                                    seat = Select(driver.find_element_by_id('SeatAssign0'))
                                    driver.implicitly_wait(5)
                                    seat.select_by_value("1")

                                    # '다음단계' 버튼 클릭
                                    # PriceSelect.Next()
                                    driver.execute_script("PriceSelect.Next()")

                                    # 좌석 선택 화면 로딩시 시간이 걸려서 상황에따라 크롤링이 안됨.
                                    driver.implicitly_wait(5)
                                    driver.switch_to.default_content()

                                    driver.implicitly_wait(20)

                                    # 좌석 리스트 출력
                                    w_flag = True
                                    iframe2 = None
                                    iframe3 = None
                                    while w_flag or iframe2 is None:
                                        try:
                                            iframe2 = WebDriverWait(driver, 5).until(
                                                cond.presence_of_element_located((By.ID, 'frmSeatSelect'))
                                            )
                                            w_flag = False
                                        except:
                                            print('again - 0')
                                            iframe2 = None
                                            w_flag = True
                                    # iframe2 = driver.find_element_by_id("frmSeatSelect")
                                    driver.switch_to.frame(iframe2)
                                    driver.implicitly_wait(20)
                                    w_flag = True
                                    while w_flag or iframe3 is None:
                                        try:
                                            iframe3 = WebDriverWait(driver, 5).until(
                                                cond.presence_of_element_located((By.ID, 'seat_dispaly'))
                                            )
                                            w_flag = False
                                        except:
                                            print('again - 1')
                                            iframe3 = None
                                            w_flag = True

                                    # iframe3 = driver.find_element_by_id("seat_dispaly")
                                    driver.switch_to.frame(iframe3)
                                    driver.implicitly_wait(20)

                                    w_flag = True
                                    # while w_flag:
                                    try:
                                        WebDriverWait(driver, 5).until(
                                            cond.presence_of_element_located((By.CSS_SELECTOR, 'body > div > img'))
                                        )
                                        seats = driver.find_elements_by_css_selector('body > div > img')
                                        w_flag = False
                                    except:
                                        print('again - 2')
                                        w_flag = True
                                        seats = []

                                    print("start-->")
                                    for s in seats:
                                        print(s.get_attribute('id'), end=' ')
                                        insert = "INSERT INTO seat(mt_id_id, s_name, s_reserved) VALUES(%s, %s, %s)"
                                        insertQueryWithoutId(insert, mt_id, s.get_attribute('id'), 0)

                                    print()

                                    driver.switch_to.default_content()
                                    driver.implicitly_wait(20)
                                    iframe2 = driver.find_element_by_id("frmSeatSelect")
                                    driver.switch_to.frame(iframe2)
                                    driver.execute_script("parent.Control.CloseSeatWindow();")
                                    print("<--end")
                                    # btn_close.click()
                                    driver.switch_to.default_content()
                                    driver.implicitly_wait(10)

                                    driver.switch_to.frame(iframe)
                                    sleep(1)
                print('———----------------')
                now_date += 1
                driver.implicitly_wait(10)
        print("finish")