from django.test import TestCase

from ..forms import CategoryForm


class CategoryFormTest(TestCase):
    """Case of testing category form"""

    def test_form_with_correct_data(self):
        """Test: does form correctly validate data"""
        data = {'title': 'test_title'}
        form = CategoryForm(data)
        self.assertTrue(form.is_valid())

    def test_form_with_incorrect_data(self):
        """Test: does form validate incorrect data"""
        data = {'title': 'x'*51}
        form = CategoryForm(data)
        self.assertFalse(form.is_valid())
