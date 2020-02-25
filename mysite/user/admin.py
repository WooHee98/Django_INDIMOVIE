from django.contrib import admin
from user.models import Userdatado, UserStatistic

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm

from django.db.models import F, Q, Sum, Max, Count, Avg, Case, When, IntegerField
from django.db.models.functions import TruncMonth
from datetime import date, datetime

#예매율 통계
from reservation.models import Seat

# Register your models here.

@admin.register(Userdatado)
class UserAdmin(admin.ModelAdmin):
    list_display = ('u_id', 'u_idtext', 'u_name', 'u_phone', 'u_birth', 'password', 'u_password')
    change_list_template = "admin/change_list.html"
    form = UserChangeForm
    add_form = UserCreationForm

    def is_writered(self, obj):
        if Sinariodatado.objects.all.filter(u_id=obj):
            return is_writered.boolean(True)

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    change_list_template = "admin/user/change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        #통계내용
        #월별통계를 위해서 월(달) 오름차순으로 정렬
        monthly_user = Userdatado.objects.annotate(
            date_key=TruncMonth('date_joined')
        ).order_by('date_key')

        # values().annotate()를 같인쓰면 Group by와 같음
        monthly_user = monthly_user.values('date_key').annotate(
            total=Count('u_id')
        )
        #print(monthly_user)

        #월별과 키 값을 나누어서 저장
        monthly_user_tmp = []
        monthly_user_key = []
        cnt = 0
        for m in monthly_user:
            monthly_user_key.append(m['date_key'].strftime('%Y-%m'))
            tmp_data = [0] * len(monthly_user)
            tmp_data[cnt] = int(m['total'])
            monthly_user_tmp.append((m['date_key'].strftime('%Y-%m'), str(tmp_data)))
            cnt += 1

        #예매건수 통계
        book_percent = Seat.objects.values('mt_id__m_id').annotate(
            booked=Count(Case(
                When(s_reserved=True, then=1),
                output_field=IntegerField()
            )),
            total=Count('mt_id')
        )

        reservations = []
        for b in book_percent:
            #예매율을 구할거면 밑에 수식에  * 100 추가
            reservations.append((b['mt_id__m_id'], b['booked'] / b['total']))
        print(reservations)

        extra_context['monthly_user_key'] = monthly_user_key
        extra_context['monthly_user_tmp'] = monthly_user_tmp
        extra_context['reservations'] = reservations

        return super().changelist_view(
            request, extra_context=extra_context,
        )
