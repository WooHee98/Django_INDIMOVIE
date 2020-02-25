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
from scenario.models import Sinariodatado

class News(models.Model):
    u_id = models.ForeignKey(Userdatado, on_delete=models.CASCADE)
    s_id = models.ForeignKey(Sinariodatado, on_delete=models.CASCADE)
    sn_title = models.CharField(max_length = 40, null=False)
    sn_content = models.TextField(null=False, blank=False)
    sn_regdate = models.DateField(auto_now_add=True)
    #n_image = ThumbnailImageField()

    class Meta:
        db_table = 'news'
