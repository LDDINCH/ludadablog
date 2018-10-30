# _*_ encoding:utf-8 _*_
__author__ = "ludada"
__date__ = "2018/10/28 21:28"
from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhost:8000/blog/
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blog_type_list, name="blog_type_list"),
    path('date/<int:year>/<int:month>', views.blog_dates_list, name="blog_date_list"),
]