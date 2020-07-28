from django.urls import path

from allauth.account import views


urlpatterns = [
    path('signup/', views.signup, name='account_signup'),
    path('login/', views.login, name='account_login'),
    path('logout/', views.logout, name='account_logout'),
]
