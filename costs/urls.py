from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetCreateCostsView.as_view(), name="all_costs"),
    path('<uuid:pk>/', views.GetUpdateDeleteCost.as_view(),
         name="concrete_cost"),
    path(
        '<int:year>/<int:month>/',
        views.GetCostsForTheMonthView.as_view(), name="month_costs"
    ),
    path(
        '<int:year>/<int:month>/<int:day>/',
        views.GetCostsForTheDateView.as_view(), name="date_costs"
    ),
    path(
        'statistic/<int:year>/<int:month>/',
        views.CostsMonthStatisticView.as_view(), name="costs_statistic_month"
    ),
    path(
        'statistic/<int:year>/',
        views.CostsYearStatisticView.as_view(), name="costs_statistic_year"
    ),
    path(
        'statistic/average/',
        views.AverageCostsView.as_view(), name="average_costs"
    ),
]
