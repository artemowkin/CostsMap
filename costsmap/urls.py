from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django AllAuth
    path('accounts/', include('accounts.urls')),

    # Local
    path('', include('costs.urls')),
]
