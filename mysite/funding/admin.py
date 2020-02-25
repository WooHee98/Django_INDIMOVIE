from django.contrib import admin
from funding.models import Fundingdatado, FundingStatistic
from user.models import Userdatado
from reservation.models import Seat
from scenario.models import Sinariodatado
from django.db.models import F, Q, Sum, Max, Count, Avg, Case, When, IntegerField
from django.db.models.functions import TruncMonth
from datetime import date, datetime

# Register your models here.

@admin.register(Fundingdatado)
class FundingAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"
    list_display = ('s_id', 'u_id', 'f_amount', 'f_created_at', 'f_credit_info_display')
    def f_credit_info_display(self, obj):
        return obj.f_cardnum + " // " + obj.f_vaildity + " // " + obj.f_cardpass

@admin.register(FundingStatistic)
class FundingStatisticAdmin(admin.ModelAdmin):
    change_list_template="admin/funding/change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        ## 통계 참고 ##
        # annotate > 모든 펀딩 row에 date_key라는 칼럼 추가
        #월별통계를 위해 date_key를 오름차순으로 정렬
        monthly = Fundingdatado.objects.annotate(
            date_key = TruncMonth('f_created_at')
        ).order_by('date_key')

        book_percent = Seat.objects.values('mt_id__m_id').annotate(
            booked=Count(Case(
                When(s_reserved=True, then=1),
                output_field=IntegerField()
            )),
            total=Count('mt_id')
        )

        reservations = []
        for b in book_percent:
            reservations.append((b['mt_id__m_id'], b['booked'] / b['total']) * 100)
        print(reservations)

        # values 선택한 값만 표시 >  select date_key from funding 과 같음
        # values().annotate()를 같인쓰면 Group by와 같음
        monthly = monthly.values('date_key').annotate(
            total=Sum('f_amount')
        )

        # aggregate > 선택한 칼럼을 기준으로 값 하나를 계산
        tmp = Fundingdatado.objects.aggregate(max=Max('f_amount'), avg=Avg('f_amount'))

        #(-)면 내림차순으로 order by가 가능
        #최고금액 후원 유저
        max_user = Fundingdatado.objects.all().order_by('-f_amount').first()
        for t in tmp:
            print(tmp[t])

        print(monthly)
        # extra_context['osm_data'] = self.get_osm_info()
        extra_context['statistic'] = tmp
        extra_context['max_user'] = max_user

        #최고금액 시나리오
        max_scenario = Sinariodatado.objects.all().order_by('-s_deposit_money').first()
        extra_context['max_scenario'] = max_scenario

        # 월별 값과 키를 나누어 저장
        monthly_key = []
        monthly_val = []
        monthly_tmp = []
        cnt = 0
        for m in monthly:
            monthly_key.append(m['date_key'].strftime('%Y-%m'))
            monthly_val.append(int(m['total']))
            tmp_data = [0] * len(monthly)
            tmp_data[cnt] = int(m['total'])
            monthly_tmp.append((m['date_key'].strftime('%Y-%m'), str(tmp_data)))
            cnt += 1


        #시나리오 성공 / 실패 / 진행중
        se_data = [0] * 3

        se_finshed = Sinariodatado.objects.filter(s_spon_date__lt=datetime.now())
        se_data[2] = Sinariodatado.objects.filter(s_spon_date__gte=datetime.now()).count()
        for t in se_finshed:
            fnd = Fundingdatado.objects.filter(s_id=t).aggregate(total=Sum('f_amount'))
            if fnd['total'] is not None and t.s_spon_money < fnd['total']:
                se_data[0] += 1
            else:
                se_data[1] += 1

        extra_context['monthly'] = monthly
        extra_context['monthly_tmp'] = monthly_tmp

        extra_context['monthly_key'] = monthly_key
        extra_context['monthly_val'] = monthly_val
        extra_context['scenario'] =str(se_data)

        return super().changelist_view(
            request, extra_context=extra_context,
        )
