from allauth.account.views import SignupView

from costs.services.categories import CategoryService


class SignupWithCategoriesView(SignupView):

    """SignUp view with setting default categories for new user"""

    service = CategoryService()

    def form_valid(self, form):
        """Add default categories for new user"""
        resp = super().form_valid(form)
        self.service.set_default_categories(owner=self.user)
        return resp
