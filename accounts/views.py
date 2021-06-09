from rest_framework.views import APIView
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView

from .serializers import UserSerializer
from categories.services.base import SetUserDefaultCategoriesService


class RegisterWithCategoriesView(RegisterView):
    """SignUp view with setting default categories for new user"""

    def perform_create(self, serializer):
        """Add default categories for new user"""
        user = super().perform_create(serializer)
        SetUserDefaultCategoriesService.execute({
            'owner': user
        })
        return user


class UserView(APIView):
    """View to display current user information"""

    def get(self, request):
        serialized_user = UserSerializer(self.request.user).data
        return Response(serialized_user)

