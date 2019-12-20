from ast import parse

from check.ast_helpers import get_names, get_variable_full_name


def test_get_names():
    node = parse('Model.objects.all().filter().order_by()').body[0].value
    assert get_names(node) == ['order_by', 'filter', 'all', 'objects', 'Model']


def test_get_names_on_name_node():
    node = parse('pedro()').body[0].value
    assert get_names(node) == ['pedro']


def test_get_variable_full_name():
    node = parse('self.pepe.juan').body[0].value
    assert get_variable_full_name(node) == 'self.pepe.juan'
