from generics.views import GetCreateGenericView, GetUpdateDeleteGenericView
from .services.base import (
    CreateCategoryService, DeleteCategoryService, ChangeCategoryService,
    GetCategoriesService
)
from .services.commands import GetAllCategoriesCommand
from .serializers import CategorySerializer


class GetCreateCategoryView(GetCreateGenericView):
    """View to get all categories and create a new category"""

    get_command = GetAllCategoriesCommand
    create_service = CreateCategoryService
    serializer_class = CategorySerializer
    model_name = 'category'


class GetUpdateDeleteCategory(GetUpdateDeleteGenericView):
    """View to get/delete/update a concrete category"""

    get_service_class = GetCategoriesService
    delete_service_class = DeleteCategoryService
    update_service_class = ChangeCategoryService
    serializer_class = CategorySerializer
    model_name = 'category'
