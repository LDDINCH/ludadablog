from django.contrib import admin
from .models import User


@admin.register(User)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'mobile')


