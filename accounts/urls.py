from django.urls import path
from django.views.decorators.cache import cache_page

from allauth.account import views

from .views import SignupWithCategoriesView


urlpatterns = [
    path('signup/', cache_page(604800)(SignupWithCategoriesView.as_view()),
         name='account_signup'),
    path('login/', cache_page(604800)(views.login), name='account_login'),
    path('logout/', cache_page(604800)(views.logout), name='account_logout'),
]
