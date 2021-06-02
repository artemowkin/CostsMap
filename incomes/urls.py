from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetCreateIncomesView.as_view(), name="all_incomes"),
    path('<uuid:pk>/', views.GetUpdateDeleteIncome.as_view(),
         name="concrete_income"),
    path('<int:year>/<int:month>/', views.GetIncomesForTheMonthView.as_view(),
         name="month_incomes"),
    path(
        '<int:year>/<int:month>/<int:day>/',
        views.GetIncomesForTheDateView.as_view(), name="date_incomes"
    ),
]
