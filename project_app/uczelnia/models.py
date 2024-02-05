from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.urls import reverse


class Department(models.Model):
    """ tutaj będą przechowywane dane dotyczące wydziałów"""
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """ Model użytkownika (studenta lub pracownika)"""
    #objects = CustomUserManager()
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    avatar = models.ImageField(default='default.png', upload_to='profile_pics')
    birthday = models.DateField(default=date(2000, 1, 1))
    phone = models.CharField(max_length=9, blank=False)
    address = models.CharField(max_length=100, blank=False)
    semester = models.CharField(max_length=100, default="2023/2024")  # semestr na którym jest student
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   null=False)  # w jakim wydziale studiuje student lub zatrudniony jest pracownik
    is_employee = models.BooleanField(default=False)  # czy użytkownik jest pracownikiem
    is_verified = models.BooleanField(default=False) #veryfikacja przez admina

    def __str__(self):
        return self.first_name + " " + self.last_name + " "


class Subject(models.Model):
    """ tutaj będą przechowywane dane dotyczące przedmiotów"""
    name = models.CharField(max_length=100, blank=False, null=False)  # nazwa przedmiotu
    purpose = models.TextField(default="")  # cel kształcenia
    effects = models.TextField(default="")  # efekty kształcenia
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # przypiany do przedmiotu nauczyciel
    semester = models.CharField(max_length=100, default="2023/2024")  # semestr na którym jest student
    ects_points = models.IntegerField(default=0, verbose_name='Punkty ECTS')

    def __str__(self):
        return self.name + ", semestr:" + self.semester + ", prowadzący: " + self.teacher.first_name + " " + self.teacher.last_name + ", wydział: " + self.teacher.department.name

    def get_absolute_url(self):
        """ funckja zwraca url """
        return reverse("subject_details", kwargs={"pk": self.pk})


class Education(models.Model):
    """ tutaj będą przechowywane dane dotyczące kształcenia studentów.
    Każdy rekord będzie zawierał informacje o tym, jaką ocenę z jakiego przedmiotu dostał student."""
    GRADE_CHOICES = [
        (2.0, '2.0'),
        (3.0, '3.0'),
        (3.5, '3.5'),
        (4.0, '4.0'),
        (4.5, '4.5'),
        (5.0, '5.0'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # którego studenta dotyczy ocena
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # z jakiego przedmiotu jest ocena
    effect = models.CharField(max_length=140, default="")
    grade = models.FloatField(choices=GRADE_CHOICES, default=2.0)

    def __str__(self):
        return self.subject.name + " " + self.effect + " " + str(
            self.grade) + self.student.first_name + " " + self.student.last_name

    def get_absolute_url(self):
        """ funckja zwraca url """
        return reverse("education_details", kwargs={"pk": self.pk})
#https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
# Metody get_absolute_url są  przydatne,
# ponieważ definiują, jak można uzyskać URL do szczegółowego widoku obiektu.
# To jest zgodne  DRY (Don't Repeat Yourself)
# bo URL jest zdefiniowany w jednym miejscu a mogę dać go w różnych miejsach
class News(models.Model):
    """ Aktualności uniwersyteckie"""
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ funckja zwraca url """
        return reverse("news_details", kwargs={"pk": self.pk})
