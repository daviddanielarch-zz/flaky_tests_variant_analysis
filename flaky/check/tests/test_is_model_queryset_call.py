from ast import parse

from check.analyze import is_model_queryset_call


def test_is_model_queryset_call():
    node = parse('TheModel.objects.filter().all()').body[0].value
    assert is_model_queryset_call(node)


def test_is_model_queryset_call_with_ordering():
    node = parse('OrderedModel.objects.filter().all()').body[0].value
    assert not is_model_queryset_call(node)


def test_is_model_queryset_call_with_order_by():
    node = parse("TheModel.objects.filter().all().order_by('name')").body[0].value
    assert not is_model_queryset_call(node)
