# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

class Movie(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_title = models.CharField(max_length=70, null=False)
    m_title_id = models.CharField(max_length=70, blank=True, null=True)
    m_genre = models.CharField(max_length=50, blank=True, null=True)
    m_runtime = models.CharField(max_length=30, blank=True, null=True)
    m_opendate = models.CharField(max_length=30, blank=True, null=True)
    m_class = models.CharField(max_length=30, blank=True, null=True)
    m_class_id = models.CharField(max_length=30, blank=True, null=True)
    m_director = models.CharField(max_length=70, blank=True, null=True)
    m_actor = models.CharField(max_length=300, blank=True, null=True)
    m_scenario = models.CharField(max_length=3000, blank=True, null=True)
    m_image_url = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'movie'
