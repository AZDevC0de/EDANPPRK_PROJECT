from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Login", max_length=150)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)