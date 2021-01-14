from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # REST Authentication
    path('auth/', include('accounts.urls')),

    # Swagger
    path('apidocs/', TemplateView.as_view(
        template_name='swagger-ui.html',
    ), name='swagger-ui'),

    # Local
    path('', include('costs.urls')),
    path('incomes/', include('incomes.urls')),
]
