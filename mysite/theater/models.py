# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models


class Theaterdatado(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=70)
    t_area = models.CharField(max_length=20)        #영화관 지역(서울, 경기 ...)
    t_address = models.CharField(max_length=100)    #영화관 상세주소
    t_phone = models.CharField(max_length=50)
    t_webaddress = models.URLField(unique=True, verbose_name='url')
    t_info = models.TextField(null=True, verbose_name='Theater Description')
    t_adult = models.CharField(max_length=10)       #영화관 성인요금
    t_kid = models.CharField(max_length=10)         #영화관 청소년요금
    #영화관 승인/미승인 여부를 확인하기 위한 컬럼
    is_confirmed = models.BooleanField(default=False, blank=True)
    t_lat= models.CharField(max_length=100) 
    t_lng= models.CharField(max_length=100) 
    
    
    class Meta:
        # managed = False
        db_table = 'theaterdatado'


