from allauth.account.views import SignupView

from costs.services.categories import SetUserDefaultCategoriesService


class SignupWithCategoriesView(SignupView):
    """SignUp view with setting default categories for new user"""

    def form_valid(self, form):
        """Add default categories for new user"""
        response = super().form_valid(form)
        SetUserDefaultCategoriesService.execute({
            'owner': self.request.user
        })
        return response
