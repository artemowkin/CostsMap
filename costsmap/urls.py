from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django AllAuth
    path('accounts/', include('accounts.urls')),

    # Local
    path('', RedirectView.as_view(url='costs/')),
    path('costs/', include('costs.urls')),
    path('incomes/', include('incomes.urls')),
    path('categories/', include('categories.urls')),
]
