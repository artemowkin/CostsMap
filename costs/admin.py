from django.contrib import admin

from .models import Cost


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('title', 'costs_sum', 'category', 'owner', 'date')
    list_filter = ('date',)
    search_fields = ('title',)
