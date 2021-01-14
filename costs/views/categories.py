from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from costs.services.categories import (
    GetCategoriesService, CreateCategoryService, ChangeCategoryService,
    DeleteCategoryService
)
from ..serializers import (
    CategorySerializer, PostCategorySerializer
)
from utils.views import DefaultView, DeleteGenericView
from costs.services.commands import GetCategoryCostsCommand


class CategoryListView(DefaultView):
    """View to return all user categories"""

    serializer = CategorySerializer

    def get(self, request):
        categories = GetCategoriesService.get_all(request.user)
        serializer = self.serializer(categories, many=True)
        return Response(serializer.data)


class CostsByCategoryView(DefaultView):
    """View to return all user category costs"""

    command = GetCategoryCostsCommand

    def get(self, request, pk):
        command = self.command(pk, request.user)
        data = command.execute()
        return Response(data)


class CreateCategoryView(DefaultView):
    """View to create a new category"""

    serializer = PostCategorySerializer

    def post(self, request):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        serializer = self.serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        try:
            category = CreateCategoryService.execute(request_data)
            return Response(serializer.data, status=201)
        except IntegrityError:
            raise ValidationError({
                "base": "The same category already exists"
            })


class ChangeCategoryView(DefaultView):
    """View to change a category"""

    serializer = PostCategorySerializer

    def post(self, request, pk):
        request_data = request.data.copy()
        request_data.update({'owner': request.user.pk})
        category = GetCategoriesService.get_concrete(pk, request.user)
        serializer = self.serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        request_data.update({'category': category})
        try:
            category = ChangeCategoryService.execute(request_data)
            return Response(serializer.data, status=201)
        except IntegrityError:
            raise ValidationError({
                "base": "The same category already exists"
            })


class DeleteCategoryView(DeleteGenericView):
    """View to delete a category"""

    object_name = 'category'
    get_service = GetCategoriesService
    delete_service = DeleteCategoryService
