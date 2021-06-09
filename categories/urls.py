from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetCreateCategoryView.as_view(), name="all_categories"),
    path('<uuid:pk>/', views.GetUpdateDeleteCategory.as_view(),
         name="concrete_category"),
    path('<uuid:pk>/costs/', views.GetCategoryCostsView.as_view(),
         name="category_costs")
]
