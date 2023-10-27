from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import LoginForm
from .models import Uzytkownikk
def strona_glowna(request):
    # aktualnosci = "[Jacek12, Janek12]"
    # return HttpResponse("To jest mój pierwszy test")
    baza = Uzytkownikk.objects.all()
    return render(request, 'strona_glowna.html', {'pierwsza': baza })


# def strona_glowna(request):
#     return render(request, 'strona_glowna.html')
# def zaloguj(request):
#     form = AuthenticationForm()
#     form = LoginForm()
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('login')
#         else:
#             return HttpResponse("Nieprawidłowe dane logowania")
#     return render(request, 'strona_glowna.html',{'text':})
#
# # def zaloguj(request):
#
#
# def wyloguj(request):
#     logout(request)
#     return redirect('strona_glowna')