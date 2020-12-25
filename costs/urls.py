from django.urls import path, register_converter
from django.views.generic.base import RedirectView

from utils import converters

from . import views


register_converter(converters.ISODateConverter, 'date')
register_converter(converters.MonthYearConverter, 'month')
register_converter(converters.YearConverter, 'year')

urlpatterns = [
    # Redirect
    path('', RedirectView.as_view(url='costs/')),

    # Costs
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
    path('costs/history/', views.CostsHistoryView.as_view(),
         name='costs_history'),
    path('costs/statistic/', views.CostsStatisticPageView.as_view(),
         name='costs_statistic_for_this_month'),
    path('costs/<month:date>/statistic/',
         views.CostsStatisticPageView.as_view(), name='costs_statistic_page'),
    path('costs/<month:date>/statistic/json/', views.StatisticView.as_view(),
         name='statistic'),
    path(
        'costs/<year:date>/statistic/json/',
        views.CostStatisticForTheLastYear.as_view(),
        name='statistic_for_the_year'
    ),

    # Categories
    path('categories/', views.CategoryListView.as_view(),
         name='category_list'),
    path('categories/add/', views.CreateCategoryView.as_view(),
         name='create_category'),
    path('categories/<uuid:pk>/costs/', views.CostsByCategoryView.as_view(),
         name='category_costs'),
    path('categories/<uuid:pk>/change/', views.ChangeCategoryView.as_view(),
         name='change_category'),
    path('categories/<uuid:pk>/delete/', views.DeleteCategoryView.as_view(),
         name='delete_category'),
]
