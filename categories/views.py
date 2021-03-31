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

    def get(self, request):
        categories = GetCategoriesService.get_all(request.user)
        return render(
            request, 'costs/category_list.html', {'categories': categories}
        )


class CostsByCategoryView(DefaultView):
    """View to render all user category costs"""

    def get(self, request, pk):
        command = GetCategoryCostsCommand(pk, request.user)
        context = command.execute()
        return render(request, 'costs/costs_by_category.html', context)


class CreateCategoryView(DefaultView):
    """View to create a new category"""

    def get(self, request):
        form = CategoryForm()
        return render(request, 'costs/add_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.cleaned_data.update({'owner': request.user})
            try:
                category = CreateCategoryService.execute(form.cleaned_data)
                return redirect(category.get_absolute_url())
            except IntegrityError:
                form.add_error(None, "The same category already exists")

        return render(request, 'costs/add_category.html', {'form': form})


class ChangeCategoryView(DefaultView):
    """View to change a category"""

    def get(self, request, pk):
        category = GetCategoriesService.get_concrete(pk, request.user)
        form = CategoryForm(instance=category)
        return render(request, 'costs/change_category.html', {
            'form': form, 'category': category
        })

    def post(self, request, pk):
        category = GetCategoriesService.get_concrete(pk, request.user)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.cleaned_data.update({'category': category})
            try:
                category = ChangeCategoryService.execute(form.cleaned_data)
                return redirect(category.get_absolute_url())
            except IntegrityError:
                form.add_error(None, 'The same category already exists')
                category = GetCategoriesService.get_concrete(pk, request.user)

        return render(request, 'costs/change_category.html', {
            'form': form, 'category': category
        })


class DeleteCategoryView(DeleteGenericView):
    """View to delete a category"""

    template_name = 'costs/delete_category.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')
    get_service = GetCategoriesService
    delete_service = DeleteCategoryService
