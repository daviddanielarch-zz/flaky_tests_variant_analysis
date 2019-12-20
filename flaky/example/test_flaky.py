import unittest

import pytest
from example.models import TheModel


class TestFlaky(unittest.TestCase):
    @pytest.mark.django_db
    def test_flaky(self):
        TheModel.objects.create(name=1)
        TheModel.objects.create(name=2)
        TheModel.objects.create(name=3)
        TheModel.objects.create(name=4)

        models = TheModel.objects.all()

        self.assertEqual(models[0].name, 1)
        self.assertEqual(models[1].name, 2)
        self.assertEqual(models[2].name, 3)
        self.assertEqual(models[3].name, 4)

    def test_flaky_with_self_vars(self):
        TheModel.objects.create(name=1)
        TheModel.objects.create(name=2)
        TheModel.objects.create(name=3)
        TheModel.objects.create(name=4)

        self.models = TheModel.objects.all()

        self.assertEqual(self.models[0].name, 1)
        self.assertEqual(self.models[1].name, 2)
        self.assertEqual(self.models[2].name, 3)
        self.assertEqual(self.models[3].name, 4)

    @pytest.mark.django_db
    def test_also_flaky_not_detected(self):
        TheModel.objects.create(name=1)
        TheModel.objects.create(name=2)

        models = TheModel.objects.all()

        model1 = models[0]
        model2 = models[1]

        self.assertEqual(model1.name, 1)
        self.assertEqual(model2.name, 2)
