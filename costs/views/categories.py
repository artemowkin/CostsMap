from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError

from ..forms import CategoryForm
from ..services.categories import CategoryService
from ..services.costs import CostService
from utils.views import CreateGenericView, DeleteGenericView, DefaultView


class CategoryListView(DefaultView):
    """View to render all user categories"""

    template_name = 'costs/category_list.html'
    context_object_name = 'categories'
    service = CategoryService()

    def get(self, request):
        categories = self.service.get_all(self.request.user)
        return render(
            request, self.template_name, {
                self.context_object_name: categories
            }
        )


class CostsByCategoryView(DefaultView):
    """View to render all user category costs"""

    template_name = 'costs/costs_by_category.html'
    context_object_name = 'costs'
    service = CategoryService()
    cost_service = CostService()

    def get(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        costs = self.service.get_category_costs(category)
        total_sum = self.cost_service.get_total_sum(costs)
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
    service = CategoryService()


class ChangeCategoryView(DefaultView):
    """View to change a category"""

    form_class = CategoryForm
    template_name = 'costs/change_category.html'
    service = CategoryService()

    def get(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        form = self.form_class(instance=category)
        return render(
            request, self.template_name, {'form': form, 'category': category}
        )

    def post(self, request, pk):
        category = self.service.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            try:
                category = self.service.change(category, form)
            except IntegrityError:
                self.add_form_exist_error(form)
                category = self.service.get_concrete(pk, request.user)
            else:
                return redirect(category.get_absolute_url())

        return render(
            request, self.template_name, {'form': form, 'category': category}
        )

    def add_form_exist_error(self, form):
        form.add_error(
            None, 'Category with the same title already exist'
        )


class DeleteCategoryView(DeleteGenericView):
    """View to delete a category"""

    template_name = 'costs/delete_category.html'
    success_url = reverse_lazy('category_list')
    service = CategoryService()
