"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from unittest import skip


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


@skip
class ProjectDictTest(TestCase):
    def test_lexeme_dict(self):
        """
        Здесь нужно будет проверить, что Лексема отдаёт правильные поля для автоматической обработки
        """
        pass


@skip
class ImportTest(TestCase):
    def test_csvfile_equality(self):
        """
        Here add csv export for a project, so to test that parsed file is identical to its input
        @return:
        """
        pass