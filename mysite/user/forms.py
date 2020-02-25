from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import Userdatado, UserManager

class UserCreationForm(
    forms.ModelForm):   # 사용자 생성 폼
     u_idtext = forms.CharField(
         label=_('u_idtext'),
         required=True,
         widget=forms.TextInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('user id text'),
                 'required': 'True',
             }
         )
     )
     u_name = forms.CharField(
         label=_('u_name'),
         required=True,
         widget=forms.TextInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('user name'),
                 'required': 'True',
             }
         )
     )
     password = forms.CharField(
         label=_('Password'),
         widget=forms.PasswordInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('Password'),
                 'required': 'True',
             }
         )
     )
     password1 = forms.CharField(
         label=_('Password'),
         widget=forms.PasswordInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('Password'),
                 'required': 'True',
             }
         )
     )
     password2 = forms.CharField(
         label=_('Password confirmation'),
         widget=forms.PasswordInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('Password confirmation'),
                 'required': 'True',
             }
         )
     )
     u_birth = forms.CharField(
         label=_('u_birth'),
         required=True,
         widget=forms.TextInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('user birth_year'),
                 'required': 'True',
             }
         )
     )
     u_phone = forms.CharField(
         label=_('u_phone'),
         required=True,
         widget=forms.TextInput(
             attrs={
                 'class': 'form-control',
                 'placeholder': _('user phone_number'),
                 'required': 'True',
             }
         )
     )

class Meta:
    model = Userdatado

    fields = ('u_idtext', 'u_name', 'u_birth', 'u_phone', 'password1', 'password2', 'password')

    def clean_password2(self):
        #두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.u_idtext = self.cleaned_data['u_idtext']
        user.u_name = self.cleaned_data['u_name']
        user.u_birth = self.cleaned_data['u_birth']
        user.u_phone = self.cleaned_data['u_phone']
        #set_password : 암호화된 password => 장고에서 사용
        user.set_password(self.cleaned_data["password1"])
        #u_password : 암호화되지않은 텍스트의 u_password => 안드로이드 로그인에서 사용
        user.u_password = self.cleaned_data['password']
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    # password = ReadOnlyPasswordHashField(
    #     label=_('Password')
    # )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = Userdatado
        fields = ('u_idtext', 'u_name', 'u_birth', 'u_phone', 'password')


    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserChangeForm, self).save(commit=False)
        user.u_idtext = self.cleaned_data['u_idtext']
        user.u_name = self.cleaned_data['u_name']
        user.u_birth = self.cleaned_data['u_birth']
        user.u_phone = self.cleaned_data['u_phone']
        user.set_password(self.cleaned_data["password"])
        user.u_password = self.cleaned_data['password']
        if commit:
            user.save()
        return user