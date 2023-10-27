from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


class Uzytkownikk(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('pracownik', 'Pracownik'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    student_id = models.CharField(max_length=100, blank=True, null=True)
    pracownik_id = models.CharField(max_length=100, blank=True, null=True)
    # imie = models.CharField(max_length=100, blank=False,null=False)
    # nazwisko = models.CharField(max_length=100,blank=False,null=False)  # Nazwisko
    # data_urodzenia = models.DateField(default=date(2000, 1, 1))

class Student(models.Model):
    user = models.OneToOneField(Uzytkownikk, on_delete=models.CASCADE, related_name='student_profile')
    wydzial = models.CharField(max_length=100)

    # def __str__(self):
    #     return f"{self.user.imie} {self.user.nazwisko}"


class Pracownik(models.Model):
    user = models.OneToOneField(Uzytkownikk, on_delete=models.CASCADE, related_name='pracownik_profile')
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    # def __str__(self):
    #     return f"{self.user.imie} {self.user.nazwisko} - {self.position}"