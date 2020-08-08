from django.urls import path, register_converter
from django.views.decorators.cache import cache_page

from utils import converters

from . import views


register_converter(converters.ISODateConverter, 'date')
register_converter(converters.MonthYearConverter, 'month')

urlpatterns = [
    path('', views.IncomesForTheDateView.as_view(),
         name='today_incomes'),
    path('<date:date>/', views.IncomesForTheDateView.as_view(),
         name='incomes_for_the_date'),
    path('add/', views.CreateIncomeView.as_view(),
         name='create_income'),
    path('<uuid:pk>/change/', views.ChangeIncomeView.as_view(),
         name='change_income'),
    path(
        '<uuid:pk>/delete/',
        cache_page(604800)(views.DeleteIncomeView.as_view()),
        name='delete_income'
    ),
    path('history/', views.IncomesHistoryView.as_view(),
         name='incomes_history'),
    path('statistic/', views.IncomesStatisticPageView.as_view(),
         name='incomes_statistic_for_this_month'),
    path('<month:date>/statistic/', views.IncomesStatisticPageView.as_view(),
        name='incomes_statistic_page'
    ),
]

