from django.contrib import admin
from theater.models import Theaterdatado
from django.contrib.admin import SimpleListFilter

# Register your models here.

class TheaterFilter(SimpleListFilter):
    title = "승인/미승인"
    parameter_name = "theater"

    def lookups(self, request, model_admin):
        return[
            ('승인','승인'),
            ('미승인', '미승인'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '승인':
            return queryset.filter(is_confirmed = True)
        elif self.value() == '미승인':
            return queryset.filter(is_confirmed = False)
        else:
            return queryset


@admin.register(Theaterdatado)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('t_name', 't_area', 't_address', 't_phone','t_webaddress','t_info', 't_adult', 't_kid', 'is_confirmed')
    list_editable = ('is_confirmed',)
    list_filter = [TheaterFilter]

