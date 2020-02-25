# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

from user.models import Userdatado
from theater.models import Theaterdatado
from movie.models import Movie

#상영관
class Screentheater(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_name = models.CharField(max_length=70, null=False)    #상영관이름
    t_id = models.ForeignKey(Theaterdatado, on_delete=models.CASCADE)      #영화관번호
    class Meta:
        db_table = 'screentheater'

#상영
class Movietime(models.Model):
    mt_id = models.AutoField(primary_key=True)
    m_id = models.ForeignKey(Movie, on_delete=models.CASCADE)       #영화번호
    st_id = models.ForeignKey(Screentheater, on_delete=models.CASCADE)    #상영관번호
    mt_day = models.DateField(blank=True, null=True)
    mt_time = models.CharField(max_length=30, blank=True, null=True)
    class Meta:
        db_table = 'movietime'

#좌석
class Seat(models.Model):
    mt_id = models.ForeignKey(Movietime, on_delete=models.CASCADE)    #상영번호
    s_name = models.CharField(max_length=30, null=False)     #좌석이름
    s_reserved = models.BooleanField(default=False, blank=True)         #좌석예매여부
    u_id = models.ForeignKey(Userdatado, on_delete=models.CASCADE)      #예약한 회원번호
    class Meta:
        db_table = 'seat'

