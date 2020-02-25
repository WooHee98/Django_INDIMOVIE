from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from user.models import Userdatado
from datetime import datetime

# Create your models here.

@python_2_unicode_compatible
class Service(models.Model):
    se_id = models.AutoField(primary_key=True)
    se_name = models.CharField(max_length=50, default=False, null=False)
    se_description = models.CharField(max_length=50)

    class Meta:
        ordering = ['se_name']

    def __str__(self):
        return self.se_name

#공지사항
class Notice(models.Model):
    n_id = models.AutoField(primary_key=True)
    n_title = models.CharField(max_length=50, null=False)
    n_regdate = models.DateTimeField('Register Date', auto_now_add=True)
    n_content = models.TextField('Notice Text')

    class Meta:
        ordering = ['n_title']

    def __str__(self):
        return self.n_title

#FAQ
class Faq(models.Model):
    faq_id = models.AutoField(primary_key=True)
    faq_title = models.CharField(max_length=50, null=False)
    faq_answer = models.TextField('Faq Answer')

    class Meta:
        ordering = ['faq_title']

    def __str__(self):
        return self.faq_title

#1:1문의
class Aques(models.Model):
    aq_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(Userdatado, on_delete=models.CASCADE)
    aq_title = models.CharField(max_length=50, null=False)
    aq_regdate = models.DateTimeField('Register Date', auto_now_add=True)
    aq_content = models.TextField('Admin-question Content')
    aq_answer = models.TextField('Admin-question Answer')

    class Meta:
        ordering = ['aq_title']

    def __str__(self):
        return self.aq_title + " " + self.u_id.u_idtext




