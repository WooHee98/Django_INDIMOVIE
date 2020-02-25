# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime

from scenario.models import Sinariodatado
from user.models import Userdatado

@python_2_unicode_compatible
class Fundingdatado(models.Model):
    f_id = models.AutoField(primary_key=True)
    s_id = models.ForeignKey('scenario.Sinariodatado', on_delete=models.CASCADE)
    u_id = models.ForeignKey('user.Userdatado', on_delete=models.CASCADE)
    f_amount = models.BigIntegerField(default=0, null=False)
    f_created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.u_id.u_idtext + " " + self.s_id.s_title
    f_cardnum = models.CharField(max_length=50)
    f_vaildity = models.CharField(max_length=20)
    f_cardpass = models.CharField(max_length=10)
    address = models.CharField(max_length=200, null=True )

    class Meta:
        db_table = 'fundingdatado'

#후원금 통계를 위한 펀딩 Proxy모델
class FundingStatistic(Fundingdatado):
    class Meta:
        proxy=True
