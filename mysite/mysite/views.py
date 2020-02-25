from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render

#어드민 로그아웃 후 홈 화면으로 리다이렉트를 위한 import문
from django.contrib.auth import logout
from django.shortcuts import redirect

#영화관 유저 등록
from theater.models import Theaterdatado
from user.models import Userdatado

#시나리오 등록
from mysite.forms import EnrollForm
from scenario.models import Sinariodatado, Scenarioreward


class HomeView(TemplateView):
    template_name = 'home.html'

#영화관등록View
class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'accounts/signup.html' # 템플릿은?
    form_class =  UserCreationForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

class RegisteredView(TemplateView): # generic view중에 TemplateView를 상속받는다.
    template_name = 'accounts/create_user_done.html' # 템플릿은?
    def post(self, request, **kwargs):
        #폼에서 입력한 내용을 어떻게 받아왔는지 확인하기 위한 print문
        print(request.POST)
        t_name = request.POST.get('t_name', '')
        t_area = request.POST.get('t_area', '')
        t_address = request.POST.get('t_address','')
        t_phone = request.POST.get('t_phone', '')
        t_webaddress = request.POST.get('t_webaddress', '')
        t_info = request.POST.get('t_info', '')
        t_adult = request.POST.get('t_adult', '')
        t_kid = request.POST.get('t_kid', '')
        tmp = Theaterdatado(
            t_name=t_name,
            #한글깨짐 해결하면 t_area로 바꾸기
            t_area= t_area,
            t_address = t_address,
            t_phone = t_phone,
            t_webaddress = t_webaddress,
            t_info = t_info,
            t_adult = t_adult,
            t_kid = t_kid
                )
        tmp.save()
        return render(request, 'create_user_done.html')

#시나리오 등록 View
class EnrollView(TemplateView):
    template_name = 'scenario/templates/scenario_done.html'
    form_class = EnrollForm
    def post(self, request, **kwargs):
        print(request.POST)
        s_title = request.POST.get('s_title', '')
        s_content = request.POST.get('s_content','')
        s_spon_money = request.POST.get('s_spon_money', '')
        s_spon_date = request.POST.get('s_spon_date', '')
        s_bank = request.POST.get('s_bank','')
        s_bank_name = request.POST.get('s_bank_name','')
        s_account = request.POST.get('s_account','')
        s_jang = request.POST.getlist('s_jang', [])
        u_introduce = request.POST.get('u_introduce','')
        s_purpose = request.POST.get('s_purpose','')
        s_core = request.POST.get('s_core','')
        s_plan = request.POST.get('s_core','')
        sw_phone = request.POST.get('sw_phone','')
        sw_email = request.POST.get('sw_email','')

        #리워드에 대한 form post처리
        s_money1 = request.POST.get('s_money1','')
        s_reward1 = request.POST.get('s_reward1', '')
        r_delivery1 = request.POST.get('r_delivery1', '') == 'on'
        s_money2 = request.POST.get('s_money2','')
        s_reward2 = request.POST.get('s_reward2', '')
        r_delivery2 = request.POST.get('r_delivery2', '') == 'on'
        s_money3 = request.POST.get('s_money3','')
        s_reward3 = request.POST.get('s_reward3', '')
        r_delivery3 = request.POST.get('r_delivery3', '') == 'on'
        s_money4 = request.POST.get('s_money4','')
        s_reward4 = request.POST.get('s_reward4', '')
        r_delivery4 = request.POST.get('r_delivery4', '') == 'on'
        s_money5 = request.POST.get('s_money5', '')
        s_reward5 = request.POST.get('s_reward5', '')
        r_delivery5 = request.POST.get('r_delivery5', '') == 'on'
        s_money6 = request.POST.get('s_money6', '')
        s_reward6 = request.POST.get('s_reward6', '')
        r_delivery6 = request.POST.get('r_delivery6', '') == 'on'
        s_money7 = request.POST.get('s_money7', '')
        s_reward7 = request.POST.get('s_reward7', '')
        r_delivery7 = request.POST.get('r_delivery7', '') == 'on'
        s_money8 = request.POST.get('s_money8', '')
        s_reward8 = request.POST.get('s_reward8', '')
        r_delivery8 = request.POST.get('r_delivery8', '') == 'on'
        tmp2 = Sinariodatado(
            s_title=s_title,
            u_id=request.user,
            s_content = s_content,
            s_spon_money = s_spon_money,
            s_spon_date = s_spon_date,
            u_introduce = u_introduce,
            s_purpose = s_purpose,
            s_core = s_core,
            s_plan = s_plan,
            s_bank = s_bank,
            s_bank_name = s_bank_name,
            s_account = s_account,
            s_jang = ",".join(s_jang),
            sw_phone = sw_phone,
            sw_email = sw_email
                )
        tmp2.save()
        tmp3 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money = s_money1,
            s_reward = s_reward1,
            r_delivery = r_delivery1
        )
        tmp3.save()
        tmp4 = Scenarioreward(
            r_id = Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money=s_money2,
            s_reward=s_reward2,
            r_delivery = r_delivery2
        )
        tmp4.save()
        tmp5 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money = s_money3,
            s_reward = s_reward3,
            r_delivery = r_delivery3
        )
        tmp5.save()
        tmp6 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money = s_money4,
            s_reward = s_reward4,
            r_delivery=r_delivery4
        )
        tmp6.save()
        tmp7 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money=s_money5,
            s_reward=s_reward5,
            r_delivery=r_delivery5
        )
        tmp7.save()
        tmp8 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money=s_money6,
            s_reward=s_reward6,
            r_delivery=r_delivery6
        )
        tmp8.save()
        tmp9 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money=s_money7,
            s_reward=s_reward7,
            r_delivery=r_delivery7
        )
        tmp9.save()
        tmp10 = Scenarioreward(
            r_id=Sinariodatado.objects.order_by('-s_id')[0].s_id,
            s_money=s_money8,
            s_reward=s_reward8,
            r_delivery=r_delivery8
        )
        tmp10.save()
        return render(request, 'scenario_done.html')


#어드민 로그아웃에 관련된 함수 작성
def admin_logout(request):
    logout(request)
    return redirect(reverse_lazy('home'))
