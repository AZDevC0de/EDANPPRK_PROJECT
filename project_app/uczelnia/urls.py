"""project_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path,include
from uczelnia import views
from .views import EducationUpdateView, EducationDetailsView, EducationListView, EducationCreateView, \
    EducationDeleteView, HomePageView, EditProfile, admin_home
from .views import SubjectListView, SubjectDetailsView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView
from .views import logout_view, NewsListView, NewsDetailsView, NewsCreateView, NewsUpdateView, NewsDeleteView,UserListView,UserDetailsView,UserUpdateView,UserDeleteView,UserPdfView
from .views import verify_user
from .views import UserVerificationListView
from .views import generate_pdf

# wzorce adresów url
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    #automatycznie dołącza zestaw URLi związanych z autentykacją użytkownika,
    # które są wbudowane w Django. W tym zestawie znajduje się też URL do mojej  strony logowania.
    path('signup/',views.signup, name='signup'),
    path('signup/edit_profile/', EditProfile.as_view(), name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    # path('verification-list/', views.UserVerificationListView.as_view(), name='verification_list'),
    # path('verify_user/', views.UserVerificationListView.as_view(), name='verification_list'),
    path('verification-list/', views.UserVerificationListView.as_view(), name='verification_list'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('signup/success/', views.registration_success, name='registration_success'),
    path('admin-home/', admin_home, name='admin_home'),
    path('user_redirect/', views.user_redirect, name='user_redirect'),



    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user_details'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('user_pdf/<int:pk>/', UserPdfView.as_view(), name='user_pdf'),
    path('pdf/<int:pk>/', views.generate_pdf, name='pdf'),



    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailsView.as_view(), name='news_details'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),


    path('education/', EducationListView.as_view(), name='education_list'),
    path('education/<int:pk>/', EducationDetailsView.as_view(), name='education_details'),
    path('education/create/', EducationCreateView.as_view(), name='education_create'),
    path('education/<int:pk>/update/', EducationUpdateView.as_view(), name='education_update'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),

    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', SubjectDetailsView.as_view(), name='subject_details'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),


]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
