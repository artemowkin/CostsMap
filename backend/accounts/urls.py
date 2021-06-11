from django.urls import path
from dj_rest_auth import views

from .views import RegisterWithCategoriesView, UserView


urlpatterns = [
    path('user/', UserView.as_view(), name='account_user'),
    path('signup/', RegisterWithCategoriesView.as_view(),
         name='account_signup'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
]
