from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django AllAuth
    path('accounts/', include('accounts.urls')),

    # ReDoc
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema-url': 'openapi-schema'}
    ), name='redoc'),

    # Redirect
    path('', RedirectView.as_view(url='costs/')),

    # Local
    path('costs/', include('costs.urls')),
    path('categories/', include('categories.urls')),
    path('incomes/', include('incomes.urls')),
]
