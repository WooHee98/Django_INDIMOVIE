# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
# from select_multiple_field.models import SelectMultipleField
from django.utils.encoding import (
    force_text, python_2_unicode_compatible)
from django.utils.translation import ugettext_lazy as _
from user.models import Userdatado

class Sinariodatado(models.Model):
    s_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(Userdatado, on_delete=models.CASCADE)
    s_jang = models.CharField(max_length=100)
    s_title = models.CharField(max_length=50)
    s_content = models.TextField()
    is_reviewed = models.BooleanField(default=False, blank=True)    #시나리오 검토/미검토 여부를 확인하기 위한 컬럼
    s_spon_money = models.BigIntegerField()                     #목표 금액
    s_spon_date = models.DateField()                            #목표 기간
    s_regdate = models.DateField(auto_now_add=True)             #시나리오 등록날짜
    s_bank = models.CharField(max_length=30)                    #시나리오 입금 은행명
    s_bank_name = models.CharField(max_length=20)               #시나리오 예금주
    s_account = models.CharField(max_length=50)                 #시나리오 계좌번호
    s_amount = models.BigIntegerField(default=0, null=False)    #총 후원금액
    #펀딩 수익금 확인
    s_deposit_money = models.BigIntegerField(default=0)         #작가에게 들어가는 입금예정금액
    #시나리오 등록정보
    u_introduce = models.TextField()
    s_purpose = models.TextField()
    s_core = models.TextField()
    s_plan = models.TextField()
    sw_phone = models.TextField(default=False)
    sw_email = models.TextField(default=False)

    class Meta:
        db_table = 'sinariodatado'

class Scenarioreward(models.Model):
    r_id = models.CharField(max_length=100)
    s_money = models.BigIntegerField(null=False)
    s_reward = models.CharField(max_length=120, null=False)
    r_delivery = models.NullBooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'scenarioreward'
