from django.contrib import admin
from .models import Uzytkownikk
from .models import Student
from .models import Pracownik

@admin.register(Uzytkownikk)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'wydzial')
    search_fields = ('user__username', 'wydzial')
#
@admin.register(Pracownik)
class PracownikAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position')
    search_fields = ('user__username', 'department', 'position')