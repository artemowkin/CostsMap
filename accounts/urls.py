from django.urls import path

from allauth.account import views

from .views import SignupWithCategoriesView


urlpatterns = [
    path('signup/', SignupWithCategoriesView.as_view(),
         name='account_signup'),
    path('login/', views.login, name='account_login'),
    path('logout/', views.logout, name='account_logout'),
]
