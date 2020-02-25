from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from api.permissions import IsAuthenticatedOrCreate
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from user.models import Userdatado
from api.models import Likemovie
from funding.models import Fundingdatado
from django.core.exceptions import ObjectDoesNotExist

from api.serializers import JoinSerializer
from api.serializers import UserSerializer, FundingSerializer, FundingAccountSerializer

from rest_framework import viewsets

from django.core.serializers.json import DjangoJSONEncoder


import pymysql
import json


def query(q):
    con = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8',
                          use_unicode=True)

    curs = con.cursor(pymysql.cursors.DictCursor)
    curs.execute(q)
    rows = curs.fetchall()

    result = []
    for row in rows:
        result.append(list(row.values()))

    con.close()
    return result

def selectQuery(q, *data):
    conn = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8',
                           use_unicode=True)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(q, data)
    rows = curs.fetchall()
    conn.close()
    return [{k: str(v) for k, v in row.items()} for row in rows]

#inesert
def insertQuery(q, *data):
    conn = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8',
                           use_unicode=True)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(q, data)
    conn.commit()
    conn.close()
    return HttpResponse('')


def deleteQuery(q, *data):
    conn = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8',
                           use_unicode=True)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(q, data)
    conn.commit()
    conn.close()
    return HttpResponse('')

# update
def updateQuery(q, *data):
    conn = pymysql.connect(host='localhost', user='root', password='qwert12345', db='indimdb', charset='utf8',
                           use_unicode=True)
    curs = conn.cursor(pymysql.cursors.DictCursor)
    curs.execute(q, data)
    conn.commit()
    conn.close()
    return HttpResponse(json.dumps((''), cls=DjangoJSONEncoder))



# 예매 영화 선택 정보
def getMovieInfo(request):
    select = "select  distinct m.* from movie m left join movietime mt on m.m_id=mt.m_id_id where mt.mt_day >= now()"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))



#  현재 상영 영화 정보
def getPreMovieInfo(request):
    select = "select  distinct m.* from movie m left join movietime mt on m.m_id=mt.m_id_id where  m.m_opendate <= now() and mt.mt_day >= now()"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))



#  상영예정작 영화 정보
def getYetMovieInfo(request):
    select = "select  * from movie where  m_opendate > curdate()"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))



# 영화 상세정보(안씀)
def getMovieDetailInfo1(request):
    select = "SELECT * FROM MOVIE where m_id = '{}'".format(request.GET['movie_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 영화 상세정보
def getMovieDetailInfo(request):
    if "u_id" in request.GET:
        select = "select m.* , (SELECT COUNT(lm.lm_id) FROM likemovie lm where lm.m_id=m.m_id and lm.u_id='{}') AS isLike from movie m where m.m_id = '{}'".format(request.GET['u_id'], request.GET['m_id'])
        result = query(select)
        return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))
    else:
        select = "SELECT * FROM MOVIE where m_id = '{}'".format(request.GET['m_id'])
        result = query(select)
        return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))



# 영화관  지역별 리스트
def getTheaterInfo(request):
    select = "SELECT * FROM Theaterdatado where is_confirmed=1"
    result = query(select)

    d = {}
    print(result)
    for cinema in result:
        if cinema[2] in d:
            d[cinema[2]].append(cinema)
        else:
            d[cinema[2]] = [cinema]
    print(d)
    result = []
    for i in d:
        result.append(d[i])

    return HttpResponse(json.dumps(result))


# 영화 상세정보
def getTheaterDetailInfo(request):
    select = "SELECT * FROM Theaterdatado where t_name = '{}'".format(request.GET['t_name'])
    result = query(select)
    return HttpResponse(json.dumps(result[0]))


# 예매 -> 영화관 지역별 리스트
def getTheaterReserInfo(request):
    select = "select distinct t.t_id, t.t_name, t.t_area , t_adult, t_kid from movietime mt left join ScreenTheater st on mt.st_id_id = st.st_id left join Theaterdatado t on t.t_id = st.t_id_id where m_id_id='{}' and  mt.mt_day >= curdate() and mt.mt_day <= curdate() + interval 5 day".format(
        request.GET['m_id'])
    result = query(select)

    d = {}
    print(result)
    for cinema in result:
        if cinema[2] in d:
            d[cinema[2]].append(cinema)
        else:
            d[cinema[2]] = [cinema]
    print(d)
    result = []
    for i in d:
        result.append(d[i])

    return HttpResponse(json.dumps(result))


# 예매 -> 영화,영화관 선택후 시간선택
def getMovieTimeReserInfo(request):
    select = "select distinct mt.mt_id, mt.mt_day from Moivetime mt left join ScreenTheater st on mt.st_id_id = st.st_id left join TheaterDataDo t on t.t_id = st.t_id_id where  m_id_id=%s and t_name=%s"
    result = selectQuery(select, request.GET['m_id'], request.GET['t_name'])
    return HttpResponse(json.dumps(result[0]))



# 예매 -> 상영관, 시간 리스트
def getSTReserInfo(request):
    select = "select distinct st.st_id, st.st_name,mt.mt_id, mt.mt_time from movietime mt left join ScreenTheater st on mt.st_id_id = st.st_id left join TheaterDataDo t on t.t_id = st.t_id_id where  m_id_id=%s and t.t_name=%s and mt.mt_day=%s"
    result = selectQuery(select, request.GET['m_id'], request.GET['t_name'], request.GET['mt_day'])

    d = {}
    print(result)
    for screen in result:
        if screen["st_id"] in d:
            d[screen["st_id"]].append(screen)
        else:
            d[screen["st_id"]] = [screen]
    print(d)
    result = []
    for i in d:
        result.append(d[i])

    return HttpResponse(json.dumps(result))




# 예매 -> 상영관, 시간 리스트2222나이 제한 test
def getSTReserInfofo(request):
    select = "select distinct st.st_id, st.st_name,mt.mt_id, mt.mt_time, mt.mt_day, m.m_id from movietime mt left join ScreenTheater st on mt.st_id_id = st.st_id left join TheaterDataDo t on t.t_id = st.t_id_id left join movie m on mt.m_id_id = m.m_id where m.m_id=%s and t.t_name=%s and mt.mt_day=%s "
    result = selectQuery(select, request.GET['m_id'], request.GET['t_name'], request.GET['mt_day'])

    d = {}
    print(result)
    for screen in result:
        if screen["st_id"] in d:
            d[screen["st_id"]].append(screen)
        else:
            d[screen["st_id"]] = [screen]
    print(d)
    result = []
    for i in d:
        result.append(d[i])

    return HttpResponse(json.dumps(result))



# 예매 -> 좌석 //필요없을수있음
def getSeatInfo2(request):
    select = "select * from seat where mt_id=%s"
    result = selectQuery(select, request.GET['mt_id'])
    return HttpResponse(json.dumps(result))


# 예매 -> 좌석
def getSeatInfo(request):
    select = "select distinct st.st_id , st.st_name from screentheater st left join movietime mt on mt.st_id_id =st.st_id where mt.mt_id=%s"
    result = selectQuery(select, request.GET['mt_id'])
    return HttpResponse(json.dumps(result))


# 회원가입
class Join(generics.CreateAPIView):
    queryset = Userdatado.objects.all()
    serializer_class = JoinSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


# 회원가입 중복확인
def getOverlapJoin(request):
    select = "select u_id, u_idtext from UserDataDo where u_idtext=%s "
    result = selectQuery(select, request.GET['u_idtext'])
    return HttpResponse(json.dumps(result[0]))



# 펀딩 삽입
class Funding(generics.CreateAPIView):
    queryset = Fundingdatado.objects.all()
    serializer_class = FundingSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

# 로그인로그인~~~~
def getUserDataDoLogin(request):
    select = "select u_id, u_idtext, u_password  from UserDataDo where u_idtext=%s and u_password=%s"
    result = selectQuery(select, request.GET['u_idtext'], request.GET['u_password'])
    return HttpResponse(json.dumps(result[0]))



# 로그인로그인~~~~testdyd
def getUserDataDoLoginin(request):
    select = "select u_id, u_idtext, u_password , u_birth from UserDataDo where u_idtext=%s and u_password=%s"
    result = selectQuery(select, request.GET['u_idtext'], request.GET['u_password'])
    return HttpResponse(json.dumps(result[0]))


# 회원
class UserViewSet(viewsets.ModelViewSet):
    queryset = Userdatado.objects.all()
    serializer_class = UserSerializer


def getuser(request):
    select = "select * from userdatado"
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 공지사항
def getNoticeInfo(request):
    select = "select * from service_notice order by n_id desc"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 공지사항  상세정보
def getNoticeDetailInfo(request):
    select = "SELECT * FROM service_notice where n_id = '{}'".format(request.GET['n_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 자주묻는질문
def getFreQueInfo(request):
    select = "select * from service_faq order by faq_id desc"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 자주묻는질문  상세정보
def getFreQueDetailInfo(request):
    select = "SELECT * FROM service_faq where faq_id = '{}'".format(request.GET['faq_id'])
    result = query(select)
    return HttpResponse(json.dumps(result[0]))


# 시나리오
def getScenarioInfo(request):
    select = "select distinct s.s_id, s.s_jang, s.s_title, s.s_regdate, s.is_reviewed , s.u_id_id, u.u_id, u.u_idtext ,s.s_spon_date from sinariodatado s left join userdatado u on s.u_id_id = u.u_id where s.is_reviewed=1 and s.s_spon_date >= now() order by s_id desc"
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 시나리오  상세정보
def getScenarioDetailInfo(request):
    select = "select distinct s.s_id, s.s_jang, s.s_title,s.s_content,s.s_regdate, s.s_spon_money,s.s_spon_date, s.s_amount, s.u_id_id, u.u_idtext ,s.u_introduce,s.sw_email,s.sw_phone,s.s_purpose,s.s_core, s.s_plan from sinariodatado s left join userdatado u on s.u_id_id = u.u_id where s_id= '{}'".format(
        request.GET['s_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 시나리오 소식 list
def getScenarioNewsInfo(request):
    select = "select n.* from news n left join sinariodatado s on n.s_id_id= s.s_id where n.s_id_id = '{}'".format(request.GET['s_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 시나리오 소식 Detail
def getScenarioNewsDetailInfo(request):
    select = "select n.* from news n left join sinariodatado s on n.s_id_id= s.s_id where n.id= '{}'".format(request.GET['sn_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))



# 시나리오 후원자수
def CountScenarioInfo(request):
    select = "select count(*) from fundingdatado where s_id_id= '{}'".format(request.GET['s_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 내가한 펀딩
def getMyFundingInfo(request):
    select = "select distinct f_id, f_amount, sd.s_id, sd.s_jang, sd.s_title, sd.u_id_id, ude.u_idtext, ud.u_id, ud.u_idtext , fd.f_cardnum, fd.f_vaildity, fd.f_cardpass from  fundingdatado fd left join userdatado ud on fd.u_id_id = ud.u_id left join sinariodatado sd on sd.s_id = fd.s_id_id  left join userdatado ude on sd.u_id_id = ude.u_id where ud.u_id='{}' order by f_id desc".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 내가한펀딩  update
def UpdateFundingView(request):
    update = "update fundingdatado set f_cardnum=%s ,  f_vaildity=%s, f_cardpass=%s where f_id=%s"
    result = updateQuery(update, request.GET['f_cardnum'],request.GET['f_vaildity'],request.GET['f_cardpass'] ,request.GET['f_id'])
    return result





# 내가한 시나리오
def getMyScenarioInfo(request):
    select = "select distinct s.s_id, s.s_jang, s.s_title,s.s_content,s.s_regdate, s.s_spon_money,s.s_spon_date, s.s_amount, s.u_id_id , u.u_id, u.u_idtext from sinariodatado s left join userdatado u on s.u_id_id = u.u_id where u_id='{}' and s.is_reviewed=1 order by s_id desc".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))




# 후원 계좌 업데이트
class FundingAccountView(generics.CreateAPIView):
    queryset =  Fundingdatado.objects.all()
    serializer_class = FundingAccountSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, pk):
        try:
            return Fundingdatado.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None): 
        event = self.get_object(pk) 
        serializer = FundingAccountSerializer(event) 
        return Response(serializer.data) 


    def put(self, request, pk, format=None): 
        Fundingdatado = self.get_object(pk) 
        serializer = FundingAccountSerializer(Fundingdatado, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



# 위시리스트 insert
def InsertWishiView(request):
    insert = "insert into LikeMovie(m_id, u_id) values (%s, %s)"
    result = insertQuery(insert, request.GET.get('m_id'),request.GET.get('u_id'))
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))

# 위시리스트 get
def getWishiView(request):
    select = "select DISTINCT lm.lm_id, m.m_id, m.m_title,m.m_genre, m.m_runtime, m.m_class, m.m_opendate,m.m_image_url, ud.u_id, ud.u_idtext from  LikeMovie lm left join userdatado ud on lm.u_id = ud.u_id left join movie m on m.m_id = lm.m_id  where ud.u_id='{}' group by m.m_id ".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 위시리스트 get-heart (필요없음)
def getWishiHeartView(request):
    select = "select  lm.lm_id,m.m_id, ud.u_id, ud.u_idtext, lm_heart from  LikeMovie lm left join userdatado ud on lm.u_id = ud.u_id left join movie m on m.m_id = lm.m_id where ud.u_id=%s and m.m_id=%s order by lm_id desc"
    result = selectQuery(select, request.GET['u_id'], request.GET['m_id'])
    return HttpResponse(json.dumps(result[0]))



# 위시리스트 delete
def DeleteWishiView(request):
    update = "delete from likemovie where lm_id=%s"
    result = deleteQuery(update, request.GET['lm_id'])
    return result



# 좌석정보
def getSeats(request):
    select = "select  s_name, s_reserved from seat where mt_id_id=%s"
    result = selectQuery(select, request.GET['mt_id'])
    return HttpResponse(json.dumps(result))



#좌석 업데이트
def updateSeats(request):
    nums = request.GET["num"]
    for i in range(int(nums)):
        seat = request.GET["seat{}".format(i)]
        print(seat)
        update = "update seat set s_reserved = 1 , u_id_id=%s where mt_id_id=%s and s_name=%s"
        updateQuery(update, request.GET["u_id"], request.GET["mt_id"], seat)
    
  
# 회원 아이디 찾기
def IDSearchView(request):
    select = " select  u_id, u_name, u_birth, u_birth1, u_birth2, u_phone  , u_idtext from userdatado where u_name=%s and u_phone=%s"
    result = selectQuery(select, request.GET['u_name'], request.GET['u_phone'])
    return HttpResponse(json.dumps(result[0]))

# 회원 패스워드 찾기
def PasswordSearchView(request):
    select = " select  u_id, u_name, u_birth, u_birth1, u_birth2, u_phone  , u_idtext from userdatado where u_name=%s and u_idtext=%s and u_phone=%s"
    result = selectQuery(select, request.GET['u_name'], request.GET['u_idtext'], request.GET['u_phone'])
    return HttpResponse(json.dumps(result[0]))

  

# 예매리스트  get
def getreserlistView(request):
    select = "select mt_id, m.m_title ,m.m_image_url, mt.mt_day, t.t_name, mt.mt_time,s.s_name, s.u_id_id , st.st_name ,count(id), s.mt_id_id from theaterdatado t left join screentheater st on st.t_id_id = t.t_id left join movietime mt on mt.st_id_id = st.st_id left join seat s on s.mt_id_id =mt.mt_id left join movie m on m.m_id=mt.m_id_id where s.s_reserved =1  AND s.u_id_id ='{}'  and mt.mt_day>=now()+1 group by s.mt_id_id ".format(request.GET['u_id']) 
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))

# 예매리스트  Detail get
def getreserdelistView(request):
    select = "select mt.mt_id, m.m_title ,m.m_image_url, mt.mt_day, t.t_name, mt.mt_time,s.s_name, s.u_id_id , st.st_name ,s.id from theaterdatado t left join screentheater st on st.t_id_id = t.t_id left join movietime mt on mt.st_id_id = st.st_id left join seat s on s.mt_id_id =mt.mt_id left join movie m on m.m_id=mt.m_id_id where s.s_reserved = 1  and mt.mt_day>=now()+1 and s.mt_id_id=%s and s.u_id_id=%s"
    result = selectQuery(select, request.GET['mt_id'], request.GET['u_id'])
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 예매리스트  Detail update
def UpdateReserDeView(request):
    update = "update seat set s_reserved = 0, u_id_id = 1 where id=%s"
    updateQuery(update,  request.GET["s_id"])
    


#회원 정보 수정 , 비밀번호변경가능 
def UserInfoupdateView(request):
    select = "select u_id, u_name,u_birth,u_birth1,u_birth2,u_phone, u_idtext  , u_password from userdatado where u_id='{}'".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


#비밀번호 업데이트
def UserpassupdateView(request):
    update = "update userdatado set u_password= %s where u_idtext=%s"
    updateQuery(update, request.GET["u_password"], request.GET["u_idtext"])



# 리뷰 insert
def InsertReviewView(request):
    insert = "insert into MovieReviewDataDo(mr_content, mr_icon, u_id, m_id) values (%s, %s, %s, %s)"
    result = insertQuery(insert, request.GET.get('mr_content'),request.GET.get('mr_icon'),request.GET.get('u_id'),request.GET.get('m_id'))
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 리뷰  get
def getReviewView(request):
    select = "select mr.mr_id, mr.mr_content, mr.mr_icon, u.u_id, mr.m_id, u.u_idtext ,mr.mr_regdate  from movie m left join MovieReviewDataDo mr on m.m_id=mr.m_id left join userdatado u on mr.u_id = u.u_id where mr.m_id ='{}' order by mr.mr_regdate desc ".format(request.GET['m_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))

# 내 리뷰  get
def getMyReviewView(request):
    select = "select mr.mr_id, mr.mr_content, mr.mr_icon, u.u_id, u.u_idtext , mr.mr_regdate , m.m_id, m.m_title, m.m_image_url from movie m left join MovieReviewDataDo mr on m.m_id=mr.m_id left join userdatado u on mr.u_id = u.u_id where u.u_id='{}' order by mr.mr_regdate desc ".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))

# 내 리뷰  delete
def DeleteMyReviewView(request):
    select = "delete from MovieReviewDataDo where mr_id='{}'".format(request.GET['mr_id'])
    result = deleteQuery(select)
    return result


# 내 리뷰  update
def UpdateMyReviewView(request):
    update = "update MovieReviewDataDo set mr_icon = %s , mr_content= %s where mr_id= %s "
    updateQuery(update, request.GET["mr_icon"], request.GET["mr_content"], request.GET["mr_id"])



# 1:1문의  insert
def InsertAdminQView(request):
    insert = "insert into service_aques(aq_title,aq_regdate,aq_content ,aq_answer,u_id_id) values (%s, now(),%s, '', %s)"
    result = insertQuery(insert, request.GET.get('aq_title'),request.GET.get('aq_content'),request.GET.get('u_id_id'))
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 1:1문의  get
def getAdminQView(request):
    select = "select * from service_aques where u_id_id='{}' ".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))



# 장르별 추천
def getJangRecommdation(request):
    select = "SELECT m.m_id,m.m_image_url, m.m_title, m.m_genre, m.m_runtime, t.t_name,mt.mt_id, mt.mt_time ,st.st_id,t.t_adult, t.t_kid,(SELECT curtime()) AS curtime, mt.mt_day,((t.t_lat-%s)*(t.t_lat-%s) + (t.t_lng-%s) * (t.t_lng-%s)) AS distance FROM movie m LEFT JOIN movietime mt ON m.m_id = mt.m_id_id LEFT JOIN ScreenTheater st ON mt.st_id_id=st.st_id LEFT JOIN TheaterDataDo t ON st.t_id_id = t.t_id WHERE t.is_confirmed =1 and m.m_genre LIKE %s AND mt.mt_day = curdate() and mt_time > curtime() and  having distance < 0.01  ORDER BY mt.mt_day ASC, mt.mt_time ASC, distance ASC"
    result = selectQuery(select, request.GET['t_lat'], request.GET['t_lat'],request.GET['t_lng'],request.GET['t_lng'] ,'%'+request.GET['jang']+'%')
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))

#위시리스트 바탕으로 추천
def getJangRecommdation2(request):


    #방법 2 : 이게 더 깔끔하겠네요!    
    #1) 사용자가 좋아요 누른 영화들의 모든 장르를 (중복되지 않게) 가져옴 -> "드라마", "액션", "드라마/액션", "드라마 스릴러", "스릴러/SF"

    #2) 가져온 영화 장르를 적절한 구분자로 여러번 자르고 중복 제거 -> ",", "/", " "  => "드라마", "액션", "스릴러", "SF"
    #3) 반복문으로 m_genre LIKE '%장르1%' and 를 이어붙임

    select = "SELECT m.m_genre FROM movie m RIGHT JOIN likemovie lm ON lm.m_id = m.m_id WHERE lm.u_id = %s"
    # 이거 유저 아이디 받아온다는 가정하에 짜도 되는거죠? 네네
    result = selectQuery(select, request.GET['u_id']) 
    genres = set()
    for genre in result:
        gen = genre['m_genre']
        candidates = gen.replace(", ", " ")
        candidates = candidates.replace(",", " ")
        candidates = candidates.replace("/", " ")
        for ca in candidates.split(" "):
            genres.add("%{}%".format(ca))

    extra = " "
    if len(genres) > 0:

	
        extra = " AND ({}) ".format(" OR ".join(["m.m_genre LIKE %s"] * len(genres)))
 
    datas = [request.GET['t_lat'], request.GET['t_lat'],request.GET['t_lng'],request.GET['t_lng']]
    datas += list(genres)
    datas = tuple(datas)
        
    select = "SELECT m.m_id,m.m_image_url, m.m_title, m.m_genre, m.m_runtime, t.t_name,mt.mt_id, mt.mt_time ,(SELECT curtime()) AS curtime, mt.mt_day,((t.t_lat-%s)*(t.t_lat-%s) + (t.t_lng-%s) * (t.t_lng-%s)) AS distance FROM movie m LEFT JOIN movietime mt ON m.m_id = mt.m_id_id LEFT JOIN ScreenTheater st ON mt.st_id_id=st.st_id LEFT JOIN TheaterDataDo t ON st.t_id_id = t.t_id WHERE  t.is_confirmed =1 and mt.mt_day = curdate() and  having distance < 0.01 and mt_time > curtime() {} ORDER BY mt.mt_day ASC, mt.mt_time ASC, distance ASC".format(extra)
    result = selectQuery(select, *datas)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))




#본영화 바탕으로 추천
def getJangRecommdation3(request):


    select = "SELECT m.m_genre FROM movie m RIGHT JOIN movieseen ms ON ms.m_id = m.m_id WHERE ms.u_id = %s"
    # 이거 유저 아이디 받아온다는 가정하에 짜도 되는거죠? 네네
    result = selectQuery(select, request.GET['u_id']) 
    genres = set()
    for genre in result:
        gen = genre['m_genre']
        candidates = gen.replace(", ", " ")
        candidates = candidates.replace(",", " ")
        candidates = candidates.replace("/", " ")
        for ca in candidates.split(" "):
            genres.add("%{}%".format(ca))

    extra = " "
    if len(genres) > 0:

	
        extra = " AND ({}) ".format(" OR ".join(["m.m_genre LIKE %s"] * len(genres)))
 
    datas = [request.GET['t_lat'], request.GET['t_lat'],request.GET['t_lng'],request.GET['t_lng'], request.GET['mt_time']]
    datas += list(genres)
    datas = tuple(datas)
        
    select = "SELECT m.m_id,m.m_image_url, m.m_title, m.m_genre, m.m_runtime, t.t_name,mt.mt_id, mt.mt_time ,st.st_id, t.t_adult, t.t_kid, mt.mt_day,((t.t_lat-%s)*(t.t_lat-%s) + (t.t_lng-%s) * (t.t_lng-%s)) AS distance FROM movie m LEFT JOIN movietime mt ON m.m_id = mt.m_id_id LEFT JOIN ScreenTheater st ON mt.st_id_id=st.st_id LEFT JOIN TheaterDataDo t ON st.t_id_id = t.t_id WHERE  t.is_confirmed =1 and mt.mt_day = curdate() and  having distance < 0.01 and mt.mt_time >= %s {} ORDER BY mt.mt_day ASC, mt.mt_time ASC, distance ASC".format(extra)
    result = selectQuery(select, *datas)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))




# 장르별 추천(가장 가까운 위치 알려주기)
def getNearLocation(request):
    select = "SELECT  t.t_name,((t.t_lat-%s)*(t.t_lat-%s) + (t.t_lng-%s) * (t.t_lng-%s)) AS distance FROM movie m LEFT JOIN movietime mt ON m.m_id = mt.m_id_id LEFT JOIN ScreenTheater st ON mt.st_id_id=st.st_id LEFT JOIN TheaterDataDo t ON st.t_id_id = t.t_id where t.is_confirmed =1 and  having distance < 0.01 ORDER BY distance ASC"
    result = selectQuery(select, request.GET['t_lat'], request.GET['t_lat'],request.GET['t_lng'],request.GET['t_lng'] )
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))



# 장르별 추천(거리 알려주기)
def getNearLocationList(request):
    select = "SELECT distinct t.t_name,t.t_lat, t.t_lng ,((t.t_lat-%s)*(t.t_lat-%s) + (t.t_lng-%s) * (t.t_lng-%s)) AS distance FROM movie m LEFT JOIN movietime mt ON m.m_id = mt.m_id_id LEFT JOIN ScreenTheater st ON mt.st_id_id=st.st_id LEFT JOIN TheaterDataDo t ON st.t_id_id = t.t_id where t.is_confirmed =1  and  having distance < 0.01 ORDER BY distance ASC"
    result = selectQuery(select, request.GET['t_lat'], request.GET['t_lat'],request.GET['t_lng'],request.GET['t_lng'] )
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 20분 지나면 예매 취소 못하기 (ReservationListDataAdapter2.java에서)
def getResercurtimeView(request):
    select = "select mt.mt_id,mt_time ,mt_day , s.s_name from movietime mt  left join seat s on s.mt_id_id= mt.mt_id where mt_id='{}' and s.id='{}'".format(request.GET['mt_id'],request.GET['s_id'])
    result = query(select)
    return HttpResponse(json.dumps((result[0]), cls=DjangoJSONEncoder))


# 20분 지나면 내가 본 영화 테이블에 저장 select(MainActivity2.java에서)
def getMtSeenMovieView(request):
    select = "select mt.mt_id,mt_time ,mt_day ,m.m_id, m.m_title,m.m_image_url,t.t_name , m.m_genre from movietime mt  left join seat s on s.mt_id_id= mt.mt_id left join movie m on m.m_id = mt.m_id_id left join screentheater st on st.st_id = mt.st_id_id left join theaterdatado t on t.t_id = st.t_id_id where s.u_id_id='{}' and curdate()<=mt.mt_day group by mt.mt_id".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 본영화 insert(MainActivity2.java에서)
def InsertMtSeenMovieView(request):
    insert = "insert into movieseen( mt_id, m_id, u_id) values (%s, %s, %s)"
    result = insertQuery(insert, request.GET.get('mt_id'),request.GET.get('m_id'),request.GET.get('u_id'))
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))




# 시나리오 검색창
def getScenarioSearch(request):
    select = "select distinct s.s_id, s.s_jang, s.s_title, s.s_regdate, s.is_reviewed , s.u_id_id, u.u_id, u.u_idtext ,s.s_spon_date from sinariodatado s left join userdatado u on s.u_id_id = u.u_id where s.is_reviewed=1 and s_title LIKE %s and s.s_spon_date >= now() order by s_id desc"
    result = selectQuery(select, '%'+request.GET['s_title']+'%')
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


    
# amount  update
def UpdateAmountView(request):
    update = "update sinariodatado set s_amount=%s where s_id=%s"
    result = updateQuery(update, request.GET['s_amount'],request.GET['s_id'])
    return result



# 본영화 숫자  get
def getmovieseenView(request):
    select = "select count(ms.mt_id) from movieseen ms left join userdatado u on u.u_id = ms.u_id where ms.u_id='{}' group by ms.mt_id".format(request.GET['u_id']) 
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


# 내가 본영화 get
def getmovieseenList(request):
    select = "select m.m_id,m.m_image_url, m.m_title,t.t_name, mt.mt_day  from movie m left join movietime mt  on mt.m_id_id = m.m_id left join screentheater st on st.st_id= mt.st_id_id left join theaterdatado t  on st.t_id_id = t.t_id left join movieseen ms on ms.mt_id =mt.mt_id where ms.u_id='{}'".format(request.GET['u_id'])
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))



# 시나리오 reward
def getScenarioreward(request):
    select = "select * from scenarioreward where r_id='{}'".format(request.GET['r_id']) 
    result = query(select)
    return HttpResponse(json.dumps((result), cls=DjangoJSONEncoder))


