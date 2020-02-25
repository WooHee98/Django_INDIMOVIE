from django.contrib import admin
from scenario.models import Sinariodatado, Scenarioreward
from user.models import Userdatado
from funding.models import Fundingdatado

#후원금액 계산과 펀딩성공여부를 진행하기 위해 필요한 계산함수 import
from django.db.models import F, Q, Sum, Max, Count, Avg, Case, When
from django.db.models.functions import TruncMonth

#시나리오 검토 확인을 위한 필터 import
from django.contrib.admin import SimpleListFilter

#시나리오 마감을 위한 import
from datetime import date, datetime

# Register your models here.

#시나리오 검토 확인
class ScenarioFilter(SimpleListFilter):
    title = "검토/미검토"
    parameter_name = "scenario"

    def lookups(self, request, model_admin):
        return[
            ('검토','검토'),
            ('미검토', '미검토'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '검토':
            return queryset.filter(is_reviewed=True)
        elif self.value() == '미검토':
            return queryset.filter(is_reviewed=False)
        else:
            return queryset

@admin.register(Sinariodatado)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('s_id', 'u_id', 's_title','s_content', 's_jang',
                    's_spon_date', 's_regdate','s_bank','s_bank_name','s_account', 's_info_display', 's_spon_money',
                    's_amount_display', 'is_reviewed','is_finshed', 's_deposit_money_display', 's_proceeds')
    list_editable = ('is_reviewed',)
    list_filter = [ScenarioFilter]

    #시나리오 입력정보(유저소개, 펀딩목적, 핵심, 진행계획)
    def s_info_display(self, obj):
        return obj.u_introduce + " // " + obj.s_purpose + " // " + obj.s_core + " // " + obj.s_plan

    #해당 시나리오에 모인 총 후원금액 계산
    def s_amount_display(self, obj):
        #s_id가 해당 시나리오의 id번호인 f_amount만 필터링으로 모아서 Sum함수를 사용해준다.
        #이를 위해선 두 가지 import문이 필요함
        tmp = Fundingdatado.objects.filter(s_id=obj).aggregate(total=Sum('f_amount'))
        #print(tmp['total'])
        #총합 금액으로 받아온 tmp를 금액계산하는 포맷에 맞춰서 포맷팅을 해준다.
        if tmp['total'] is not None:
            obj.s_amount = tmp['total']
            obj.save()
            return tmp['total']
        else :
            return 0

    #시나리오 펀딩이 성공했는지 확인
    def is_finshed(self, obj):
        # s_id가 해당 시나리오의 id번호인 f_amount만 필터링으로 모아서 Sum함수를 사용해준다.
        tmp = Fundingdatado.objects.filter(s_id=obj).aggregate(total=Sum('f_amount'))
        #총합 금액으로 받아온 tmp를 해당 시나리오의 s_spon_money와 비교해서 is_finished컬럼에 표시할 텍스트를 정해준다.
        #그냥 표시하면 tmp[total]금액이 없을 때, 0원을 리턴하는게 아니라 None타입으로 리턴되기 때문에, if문에 and앞 문장을 추가해준다.
        if tmp['total'] is not None and obj.s_spon_money < tmp['total']:
            return "Finish"
        else:
            return "Continue"

    #시나리오 마감확인
    def s_deposit_money_display(self, obj):
        print(obj.s_spon_date)
        if obj.s_spon_date < datetime.now().date():
            fnd = Fundingdatado.objects.filter(s_id=obj).aggregate(total=Sum('f_amount'))
            if fnd['total'] is not None and obj.s_spon_money <= fnd['total']:
                fee = fnd['total'] * 0.97
                obj.s_deposit_money = fee
                obj.save()
                return round(fee,2)
            else :
                return 0

    #수익금 확인
    def s_proceeds(self, obj):
        if obj.s_spon_date < datetime.now().date():
            fnd = Fundingdatado.objects.filter(s_id=obj).aggregate(total=Sum('f_amount'))
            if fnd['total'] is not None and obj.s_spon_money <= fnd['total']:
                fee = fnd['total'] * 0.03
                return "성공, 수수료=" + str(round(fee,2)) + ""
            else:
                return "실패"
        else:
            return "진행중"

