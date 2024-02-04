# forms.py

from django import forms
from .models import Education, Subject, News
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EducationUpdateForm(forms.ModelForm): #aktualizacja oceny (uzywany w widoku)
    class Meta:
        model = Education
        fields = ['grade']
        labels = {'grade': 'Ocena'}


class NewsUpdateForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           label='Data') #dodaje pole DateField (domyślna teraźniejsza data)

    class Meta:
        model = News
        fields = ['title', 'date', 'body'] #pola modelu uwzględnione w formularzu
        labels = {'title': 'Tytuł', 'body': 'Treść'} #etykietki


class NewsCreateForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                           label='Data') #dałam widget DateInput z atrybutem HTML type='date' dla łatwiejszego wyboru daty

    class Meta:
        model = News
        fields = ['title', 'date', 'body']
        labels = {'title': 'Tytuł', 'body': 'Treść'}


class SubjectUpdateForm(forms.ModelForm):
    ects_points = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Punkty ECTS'}),
        label='Punkty ECTS'
    )

    class Meta:
        model = Subject
        fields = ['name', 'purpose', 'effects', 'semester', 'ects_points']
        labels = {'name': 'Nazwa', 'purpose': 'Cel', 'effects': 'Efekt', 'semester': 'Semestr'}


class SubjectCreateForm(forms.ModelForm):
    ects_points = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Punkty ECTS'}),
        label='Punkty ECTS'
    )
    class Meta:
        model = Subject
        fields = ['name', 'purpose', 'effects', 'semester', 'ects_points']
        labels = {'name': 'Nazwa', 'purpose': 'Cel', 'effects': 'Efekt', 'semester': 'Semestr'}


class SignupForm(UserCreationForm):
    """ Formularz rejestracji użytkownika"""

    username = forms.CharField(
        max_length=200, required=True, help_text='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika'}),
        label='Nazwa użytkownika')

    email = forms.EmailField(help_text='',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), )
    first_name = forms.CharField(max_length=100, required=True, help_text='',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imię'}),
                                 label='Imię')

    last_name = forms.CharField(max_length=100, required=True, help_text='',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwisko'}),
                                label='Nazwisko')

    birthday = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'})
                               , label='Data urodzenia')

    phone = forms.CharField(max_length=100, required=True, help_text='',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}),
                            label='Telefon')
    address = forms.CharField(max_length=100, required=True, help_text='',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adres'}),
                              label='Adres')
    is_employee = forms.BooleanField(help_text='', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
                                     label='Czy jesteś pracownikiem')

    password1 = forms.CharField(help_text='Hasło musi zawierać małą, dużą literę oraz cyfrę', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
                                label='Hasło')
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
                                label='Powtórz hasło')

    # hihi

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'phone', 'address', 'password1',
                  'password2', 'is_employee', 'department']




