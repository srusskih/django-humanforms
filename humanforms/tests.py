from django.test import TestCase
from django import forms
from .forms import HumanMixin


class TestHumanMixin(TestCase):
    """ testing robot protection """
    def test_validation_fail(self):

        class F(HumanMixin, forms.Form):
            data = forms.CharField()

        with self.settings(ROBOT_PROTECTION=False):
            # field can be presented or not presented
            # if main data is valid - then form is valid
            self.assertTrue(F({'data': '1', 'human_question': '1'}).is_valid())
            self.assertTrue(F({'data': '1'}).is_valid())

        with self.settings(ROBOT_PROTECTION=True):
            # field have got to be presented in data, empty or with something
            self.assertFalse(F({'data': '1'}).is_valid())
            self.assertTrue(F({'data': '1', 'human_question': ''}).is_valid())
            self.assertTrue(F({'data': '1', 'human_question': '1'}).is_valid())
