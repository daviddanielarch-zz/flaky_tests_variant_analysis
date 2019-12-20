from ast import parse

from ..analyze import has_numeric_subscript


def test_check_subscript_over_call():
    node = parse('self.assertEqual(pepe[0], 2)').body[0].value
    arguments = node.args
    assert any([has_numeric_subscript(node) for node in arguments])


def test_variable_in_variable_list():
    node = parse('pepe[0]').body[0].value
    assert has_numeric_subscript(node)


def test_variable_in_variable_list_with_attr_access():
    node = parse('pepe[0].name').body[0].value
    assert has_numeric_subscript(node)


def test_non_numeric_subscript():
    node = parse('pepe[asd]').body[0].value
    assert not has_numeric_subscript(node)


def test_numeric_subscript_on_attr():
    node = parse('self.pepe[0]').body[0].value
    assert has_numeric_subscript(node)
