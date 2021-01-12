from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError

import services.common as common_services
import costs.services.categories as category_services
import costs.services as cost_services
from ..forms import CategoryForm
from ..models import Category
from utils.views import (
    CreateGenericView, DeleteGenericView, DefaultView, ChangeGenericView
)


class CategoryListView(DefaultView):
    """View to render all user categories"""

    model = Category
    template_name = 'costs/category_list.html'
    context_object_name = 'categories'

    def get(self, request):
        categories = common_services.get_all_user_entries(
            self.model, request.user
        )
        return render(
            request, self.template_name, {
                self.context_object_name: categories
            }
        )


class CostsByCategoryView(DefaultView):
    """View to render all user category costs"""

    model = Category
    template_name = 'costs/costs_by_category.html'
    context_object_name = 'costs'

    def get(self, request, pk):
        category = common_services.get_concrete_user_entry(
            self.model, pk, request.user
        )
        costs = category_services.get_category_costs(category)
        total_sum = cost_services.get_total_sum(costs)
        return render(
            request, self.template_name, {
                self.context_object_name: costs,
                'category': category, 'total_sum': total_sum
            }
        )


class CreateCategoryView(CreateGenericView):
    """View to create a new category"""

    form_class = CategoryForm
    template_name = 'costs/add_category.html'
    model = Category


class ChangeCategoryView(ChangeGenericView):
    """View to change a category"""

    form_class = CategoryForm
    template_name = 'costs/change_category.html'
    context_object_name = 'category'
    model = Category


class DeleteCategoryView(DeleteGenericView):
    """View to delete a category"""

    template_name = 'costs/delete_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')
    model = Category
