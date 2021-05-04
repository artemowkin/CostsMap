from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetCreateCostsView.as_view(), name="all_costs"),
    path('<uuid:pk>/', views.GetUpdateDeleteCost.as_view(),
         name="concrete_cost"),
    path(
        '<int:year>/<int:month>/',
        views.GetForTheMonthView.as_view(), name="month_costs"
    ),
    path(
        '<int:year>/<int:month>/<int:day>/',
        views.GetForTheDateView.as_view(), name="date_costs"
    ),
    path(
        'statistic/<int:year>/<int:month>/',
        views.CostsDateStatisticView.as_view(), name="costs_statistic"
    ),
    path(
        'statistic/average/',
        views.AverageCostsView.as_view(), name="average_costs"
    ),
]
