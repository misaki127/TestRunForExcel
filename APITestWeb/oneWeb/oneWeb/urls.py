"""oneWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from APITestWeb import views
from django.urls import include,path
from UserDao import views as Uviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/',views.upload),
    path('download/',views.download_template),
    path('download/use/',views.download_user),
    path('getCodeFile/',views.getCodeFile),
    path('uploadFile/',views.upload),
    path('download/report/',views.download_report),
    path('runTest/download/',views.download_code),
     path('login/',Uviews.logins),
    path('index/',Uviews.index),
    path('login/',auth_views.LoginView.as_view()),
    path('logout/',Uviews.logouts),
    path('createUser/',Uviews.createUser),
    path('remakePassword/',Uviews.remakePassword),
    path('forgetPassword/',Uviews.forgetPassword),
    path('runTestCase/',views.RunTestCase),
]
