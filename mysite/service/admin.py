from django.contrib import admin
from service.models import Service, Notice, Faq, Aques

# Register your models here.


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('n_id','n_title','n_regdate','n_content')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('faq_id', 'faq_title', 'faq_answer')

@admin.register(Aques)
class AquesAdmin(admin.ModelAdmin):
    list_display = ('aq_id', 'u_id', 'aq_title', 'aq_regdate', 'aq_content', 'aq_answer')

