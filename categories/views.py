"""Module with categories views"""

from django.shortcuts import render

from utils.views import (
    RenderAuthorizedView,
    CreateView,
    ChangeView,
    DeleteView
)

from .services import CategoryService
from costs.services import CostService


class CategoryListView(RenderAuthorizedView):

    """View to return all categories

    Attributes
    ----------
    service : Service
        Category's service

    template_name : str
        Template to display all categories

    """

    service = CategoryService()
    template_name = 'costs/category_list.html'

    def get(self, request):
        """Return categories list"""
        categories = self.service.get_all(owner=request.user)
        context = {'categories': categories}
        return render(request, self.template_name, context)


class CostsByCategoryView(RenderAuthorizedView):

    """View to return all category costs

    Attributes
    ----------
    service : Service
        Category's service

    template_name : str
        Template to display costs

    """

    service = CategoryService()
    cost_service = CostService()
    template_name = 'costs/costs_by_category.html'

    def get(self, request, pk):
        """Show page with all category costs"""
        costs = self.service.get_category_costs(pk, request.user)
        category = self.service.get_concrete(pk, request.user)
        total_sum = self.cost_service.get_total_sum(costs)
        return render(
            request, self.template_name,
            {'costs': costs, 'category': category, 'total_sum': total_sum}
        )


class CreateCategoryView(CreateView):

    """View to create a new category

    Attributes
    ----------
    service : Service
        Category's service

    template_name : str
        Template with form to create a new category

    """

    service = CategoryService()
    template_name = 'costs/add_category.html'


class ChangeCategoryView(ChangeView):

    """View to change a category

    Attributes
    ----------
    service : Service
        Category's service

    template_name : str
        Template with form to change a category

    context_object_name : str
        Name of category object in template

    """

    service = CategoryService()
    template_name = 'costs/change_category.html'
    context_object_name = 'category'


class DeleteCategoryView(DeleteView):

    """View to delete a category

    Attributes
    ----------
    service : Service
        Category's service

    template_name : str
        Template with form to delete a category

    context_object_name : str
        Name of category object in template

    """

    service = CategoryService()
    template_name = 'costs/delete_category.html'
    context_object_name = 'category'

