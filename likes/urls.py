# _*_ encoding:utf-8 _*_
__author__ = "ludada"
__date__ = "2018/10/29 14:20"
from django.urls import path
from . import views


urlpatterns = [
    path('like_change', views.like_change, name='like_change')
]