from django.urls import path, register_converter

from utils import converters

from . import views


register_converter(converters.ISODateConverter, 'date')
register_converter(converters.MonthYearConverter, 'month')

urlpatterns = [
    path('', views.CostsForTheDateView.as_view(),
         name='today_costs'),
    path('<date:date>/', views.CostsForTheDateView.as_view(),
         name='costs_for_the_date'),
    path('add/', views.CreateCostView.as_view(),
         name='create_cost'),
    path('<uuid:pk>/change/', views.ChangeCostView.as_view(),
         name='change_cost'),
    path('<uuid:pk>/delete/', views.DeleteCostView.as_view(),
         name='delete_cost'),
    path('history/', views.CostsHistoryView.as_view(),
         name='costs_history'),
    path('statistic/', views.CostsStatisticPageView.as_view(),
         name='costs_statistic_for_this_month'),
    path('<month:date>/statistic/',
         views.CostsStatisticPageView.as_view(), name='costs_statistic_page'),
    path('<month:date>/statistic/json/', views.StatisticView.as_view(),
         name='statistic'),
]

