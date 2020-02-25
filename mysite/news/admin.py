from django.contrib import admin

from news.models import News
from user.models import Userdatado
from scenario.models import Sinariodatado

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('u_id','s_id','sn_title','sn_content','sn_regdate')
    
