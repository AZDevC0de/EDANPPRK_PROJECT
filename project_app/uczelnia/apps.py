from django.apps import AppConfig
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class UczelniaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uczelnia'


class MyAppConfig(AppConfig):
    name = 'project_app'

    def ready(self):
        # Rejestruj czcionkę tutaj
        pdfmetrics.registerFont(TTFont('DejaVuSans', r'C:\Users\user\Desktop\My_Repozitories\EDANPPRK_PROJECT\project_app\uczelnia\static\arial.ttf'))
