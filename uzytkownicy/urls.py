
# from django.urls import path
# from uzytkownicy.views import zaloguj, wyloguj, strona_glowna

# urlpatterns = [
#
#     path('strona_glowna/',strona_glowna,name='strona_glowna'),
#     path('login/',zaloguj, name='login'),
#     path('wyloguj/',wyloguj,name='wyloguj')
# ]
from django.urls import path,include
# from django.contrib.auth import views as auth_views
from uzytkownicy.views import strona_glowna
urlpatterns = [

    path('glowna/', strona_glowna, name="strona_glowna")
    # path('uzytkownicy/',include('uzytkownicy.urls')),
    # path('login/', auth_views.LoginView.as_view(),name='login_view')

]
