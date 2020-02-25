#시나리오 등록을 위한 모델 폼 작성

from django import forms

# from user.models import Userdatado
from scenario.models import Sinariodatado

class EnrollForm(forms.ModelForm):
    model = Sinariodatado
    fields = ('s_title', 's_jang','s_content','s_spon_money','s_spon_date','s_bank','s_bank_name','s_account', 'u_introduce','s_purpose', 's_core','s_plan')
    #'u_introduce','s_purpose', 's_core','s_plan'