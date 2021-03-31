from django.urls import path

from . import views


urlpatterns = [
    path('', views.CategoryListView.as_view(),
         name='category_list'),
    path('add/', views.CreateCategoryView.as_view(),
         name='create_category'),
    path('<uuid:pk>/costs/', views.CostsByCategoryView.as_view(),
         name='category_costs'),
    path('<uuid:pk>/change/', views.ChangeCategoryView.as_view(),
         name='change_category'),
    path('<uuid:pk>/delete/', views.DeleteCategoryView.as_view(),
         name='delete_category'),
]
