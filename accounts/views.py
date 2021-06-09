from dj_rest_auth.registration.views import RegisterView

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
