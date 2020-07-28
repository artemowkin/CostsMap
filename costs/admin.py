from django.contrib import admin

from .models import Cost, Category, Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('incomes_sum', 'owner')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    search_fields = ('title',)


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('title', 'costs_sum', 'category', 'owner', 'date')
    list_filter = ('date',)
    search_fields = ('title',)

