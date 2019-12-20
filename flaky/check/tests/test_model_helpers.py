from check.model_helpers import is_django_model, has_django_model_ordering
from example.models import TheModel, OrderedModel


def test_is_django_model():
    assert is_django_model(TheModel)


def test_is_no_django_model():
    class NoModel(object):
        pass

    assert not is_django_model(NoModel)


def test_has_django_model_ordering_regular_model():
    assert not has_django_model_ordering(TheModel)


def test_has_django_model_ordering_ordered_model():
    assert has_django_model_ordering(OrderedModel)
