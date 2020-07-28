from django.urls import path, register_converter
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

from . import views, converters


register_converter(converters.ISODateConverter, 'date')

urlpatterns = [
    # Costs
    path('', RedirectView.as_view(url='costs/')),
    path('costs/', views.CostsForTheDateView.as_view(),
         name='today_costs'),
    path('costs/<date:date>/', views.CostsForTheDateView.as_view(),
         name='costs_for_the_date'),
    path('costs/add/', views.CreateCostView.as_view(),
         name='create_cost'),
    path('costs/<uuid:pk>/change/', views.ChangeCostView.as_view(),
         name='change_cost'),
    path('costs/<uuid:pk>/delete/', views.DeleteCostView.as_view(),
         name='delete_cost'),

    # Incomes
    path('incomes/', views.IncomesForTheDateView.as_view(),
         name='today_incomes'),
    path('incomes/<date:date>/', views.IncomesForTheDateView.as_view(),
         name='incomes_for_the_date'),
    path('incomes/add/', views.CreateIncomeView.as_view(),
         name='create_income'),
    path('incomes/<uuid:pk>/change/', views.ChangeIncomeView.as_view(),
         name='change_income'),
    path('incomes/<uuid:pk>/delete/', views.DeleteIncomeView.as_view(),
         name='delete_income'),

    # Categories
    path('categories/', views.CategoryListView.as_view(),
         name='category_list'),
    path('categories/add/', views.CreateCategoryView.as_view(),
         name='create_category'),
    path('categories/<uuid:pk>/change/', views.ChangeCategoryView.as_view(),
         name='change_category'),
    path('categories/<uuid:pk>/delete/', views.DeleteCategoryView.as_view(),
         name='delete_category'),
    path('history/', views.CostsHistoryView.as_view(),
         name='costs_history'),

    # Statistic
    path('statistic/json/', views.StatisticView.as_view(), name='statistic'),
    path('statistic/costs/', views.CostsStatisticPageView.as_view(),
         name='costs_statistic_page'),
    path('statistic/incomes/', views.IncomesStatisticPageView.as_view(),
         name='incomes_statistic_page'),
]

