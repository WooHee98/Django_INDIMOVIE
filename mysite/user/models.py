# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    #Userdatado 테이블에서 not null인 컬럼은 반드시 포함해야 함.
    def create_user(self, u_idtext, u_name, u_birth, u_phone, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """


        user = self.model(
            u_idtext=u_idtext,
            u_name=u_name,
            u_birth=u_birth,
            u_phone=u_phone,
        )
        user.set_password(password)
        user.u_password(user.password)
        user.save(using=self._db)
        return user

    def create_superuser(self, u_idtext, u_name, u_birth, u_phone, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.model(
            u_idtext=u_idtext,
            u_name=u_name,
            u_birth=u_birth,
            u_phone=u_phone
        )
        user.set_password(password)
        user.u_password= user.password
        user.is_superuser = True
        user.save(using=self._db)
        return user

"""
abstract base 말고 직접 abstractuser를 상속받아 이용가능
class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.email
"""


class Userdatado(AbstractBaseUser, PermissionsMixin):
    u_id = models.AutoField(primary_key=True)
    u_idtext = models.CharField(max_length=15, null=False, unique=True)
    u_password = models.CharField(max_length=128, null=False)
    u_name = models.CharField(max_length=15, null=False)
    u_birth = models.CharField(max_length=10, null=False)
    u_birth1 = models.CharField(max_length=10)
    u_birth2 = models.CharField(max_length=10)
    u_phone = models.CharField(max_length=20, null=False)
    is_writered = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    salt = models.CharField(
        verbose_name=_('Salt'),
        max_length=10,
        blank=True
    )


    objects = UserManager()

    USERNAME_FIELD = 'u_idtext'
    REQUIRED_FIELDS = ['u_name', 'u_birth', 'u_phone', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)
        db_table = 'userdatado'

    def __str__(self):
        return self.u_name

    def get_full_name(self):
        return self.u_name

    def get_short_name(self):
        return self.u_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')


#회원수와 예매율 통계를 위한 proxy모델
class UserStatistic(Userdatado):
    class Meta:
        proxy = True
