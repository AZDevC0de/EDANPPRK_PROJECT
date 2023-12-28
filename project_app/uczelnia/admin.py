from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm
from .models import CustomUser,Subject,Education,News,Department
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode


admin.site.register(Subject)
admin.site.register(Education)
admin.site.register(News)
admin.site.register(Department)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_employee', 'is_verified')

    #

admin.site.register(CustomUser, CustomUserAdmin)