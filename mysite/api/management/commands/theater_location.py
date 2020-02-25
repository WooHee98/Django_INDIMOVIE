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

        import requests
        import json
        import pymysql
        from urllib import parse

        def selectQuery(q, *data):
            conn = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb',
                                   charset='utf8', use_unicode=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(q, data)
            rows = curs.fetchall()
            conn.close()
            return [{k: str(v) for k, v in row.items()} for row in rows]

        # update
        def updateQuery(q, *data):
            conn = pymysql.connect(host='localhost', user='myuser', password='a1234567', db='indimdb',
                                   charset='utf8',
                                   use_unicode=True)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(q, data)
            conn.commit()
            conn.close()

        def getLocation(address):
            url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?{}"
            params = [("key", "AIzaSyB1CFA7Uv7Dbgg-V9C3my9l1dg69jAHRIQ"),
                      ("input", address),
                      ("inputtype", "textquery"),
                      ("fields", "geometry")]

            data = parse.urlencode(params, encoding='UTF-8', doseq=True)
            res = requests.get(url.format(data))
            result = json.loads(res.text)
            if result["status"] == "OK":
                location = result["candidates"][0]["geometry"]["location"]
                return location
            else:
                print(address)
                return None

        theaters = selectQuery("select * from theaterdatado order by t_id")

        for th in theaters:
            t_id = th["t_id"]
            address = th["t_address"]
            print(address)

            address = address[:address.find("(")].strip()
            location = getLocation(address)
            if location is None:
                print(th["t_address"])
            updateQuery("update theaterdatado set t_lat=%s, t_lng=%s where t_id=%s", location["lat"], location["lng"],
                        t_id)
            print(location["lat"])
            print(location["lng"])
