from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError

from .services.categories import (
    GetCategoriesService, CreateCategoryService, ChangeCategoryService,
    DeleteCategoryService
)
from .forms import CategoryForm
from utils.views import DefaultView, DeleteGenericView
from categories.services.commands import GetCategoryCostsCommand


class CategoryListView(DefaultView):
    """View to render all user categories"""

    template_name = 'costs/category_list.html'
    context_object_name = 'categories'

    def get(self, request):
        categories = GetCategoriesService.get_all(request.user)
        return render(
            request, self.template_name, {
                self.context_object_name: categories
            }
        )


class CostsByCategoryView(DefaultView):
    """View to render all user category costs"""

    template_name = 'costs/costs_by_category.html'
    command = GetCategoryCostsCommand

    def get(self, request, pk):
        command = self.command(pk, request.user)
        context = command.execute()
        return render(request, self.template_name, context)


class CreateCategoryView(DefaultView):
    """View to create a new category"""

    form_class = CategoryForm
    template_name = 'costs/add_category.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.cleaned_data.update({'owner': request.user})
            try:
                category = CreateCategoryService.execute(form.cleaned_data)
                return redirect(category.get_absolute_url())
            except IntegrityError:
                form.add_error(None, "The same category already exists")

        return render(request, self.template_name, {'form': form})


class ChangeCategoryView(DefaultView):
    """View to change a category"""

    form_class = CategoryForm
    template_name = 'costs/change_category.html'

    def get(self, request, pk):
        category = GetCategoriesService.get_concrete(pk, request.user)
        form = self.form_class(instance=category)
        return render(
            request, self.template_name, {'form': form, 'category': category}
        )

    def post(self, request, pk):
        category = GetCategoriesService.get_concrete(pk, request.user)
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.cleaned_data.update({'category': category})
            try:
                category = ChangeCategoryService.execute(form.cleaned_data)
                return redirect(category.get_absolute_url())
            except IntegrityError:
                form.add_error(None, 'The same category already exists')
                category = GetCategoriesService.get_concrete(pk, request.user)

        return render(
            request, self.template_name, {'form': form, 'category': category}
        )


class DeleteCategoryView(DeleteGenericView):
    """View to delete a category"""

    template_name = 'costs/delete_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')
    get_service = GetCategoriesService
    delete_service = DeleteCategoryService
