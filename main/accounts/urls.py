from django.urls import path
from . import views
from django.contrib.auth.views import (
  LoginView, LogoutView
)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/',LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('league_form/', views.LeagueFormView.as_view(), name='league_form'),
    path('league/<str:name>/', views.LeagueView.as_view(), name="league"),
    path('challenge_form/', views.ChallengeFormView.as_view(),name='challenge_form'),
    path('challenge_selector/', views.ChallengeSelectorView.as_view(),name='challenge_selector')
]
