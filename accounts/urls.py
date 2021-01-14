from django.urls import path
from django.views.decorators.cache import cache_page
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

from .views import SignupWithCategoriesView


urlpatterns = [
    path('signup/', RegisterView.as_view(),
         name='account_signup'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
]
