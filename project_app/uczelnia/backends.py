from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class VerifiedUserBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Sprawdzamy, czy użytkownik jest zweryfikowany
        return user.is_active and user.is_verified

#https://docs.djangoproject.com/en/5.0/topics/auth/customizing/