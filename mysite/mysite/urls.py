"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include

from mysite.views import HomeView

#import admin_logout추가
from mysite.views import CreateUserView, RegisteredView, EnrollView, admin_logout #EnrollmentView

#rest api
from rest_framework import routers
from api import views

app_name = 'indimovie'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # 어드민 로그아웃이 무조건 admin경로보다 위에 있어야 인식하고 바로 리다이렉트가 된다.
    url(r'^admin/logout/$', admin_logout),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),

    # 장고에서 기본적으로 제공하는 로그인, 로그아웃 기능을 포함한 url
    url(r'^accs/', include('django.contrib.auth.urls')),

    #영화관 유저 등록을 위한 url
    url(r'^accounts/signup$', CreateUserView.as_view(), name = 'signup'),
    url(r'^accounts/login/done$', RegisteredView.as_view(), name = 'create_user_done'),


    #api를 위한 url
    url(r'^movie/', include('api.urls')),
    url(r'^', include(router.urls)),

    #시나리오 등록을 위한 url
    url(r'^accounts/scenario$', EnrollView.as_view(),  name = 'scenario_enroll'),
    #url(r'^accounts/scenario/done$', EnrolledView.as_view(), name='scenario_done'),
]
