from allauth.account.views import SignupView

from costs import services


class SignupWithCategoriesView(SignupView):
    """SignUp view with setting default categories for new user

    Methods
    -------
    form_valid(form)
        Add default categories for new user

    """

    def form_valid(self, form):
        """Add default categories for new user"""
        resp = super().form_valid(form)
        services.set_user_default_categories(self.user)
        return resp
