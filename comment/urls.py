# _*_ encoding:utf-8 _*_
__author__ = "ludada"
__date__ = "2018/10/29 14:13"
from django.urls import path
from . import views


urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment')
]