from ast import parse

from ..analyze import get_numeric_subscript_variable_name_and_index, is_assert_equal, is_flaky


def test_get_subscript_variable_name_and_index():
    node = parse('pepe[0]').body[0].value
    assert get_numeric_subscript_variable_name_and_index(node) == ('pepe', 0)


def test_get_all_variables_indexes():
    code = """
self.assertEqual(juan[1], 1)
self.assertEqual(juan[2], 2)
self.assertEqual(pepe[1], 1)
self.assertEqual(pepe[5], 2)
    """

    nodes = parse(code).body
    for node in nodes:
        assert is_assert_equal(node)


def test_is_flaky():
    code = """
juan = TheModel.objects.all()
self.assertEqual(juan[1], 1)
self.assertEqual(juan[2], 2)
self.assertEqual(pepe[1], 1)
self.assertEqual(pepe[5], 2)
    """
    nodes = parse(code)
    assert is_flaky(nodes)


def test_no_flaky_single_ocurrence():
    code = """
juan = TheModel.objects.all()
self.assertEqual(juan[1], 1)
self.assertEqual(pepe[1], 1)
self.assertEqual(pepe[5], 2)
    """
    nodes = parse(code)
    assert not is_flaky(nodes)


def test_no_flaky_order_by():
    code = """
juan = TheModel.objects.all().order_by('name')
self.assertEqual(juan[1], 1)
self.assertEqual(juan[2], 2)
self.assertEqual(pepe[1], 1)
self.assertEqual(pepe[5], 2)
    """
    nodes = parse(code)
    assert not is_flaky(nodes)


def test_no_flaky_ordering():
    code = """
juan = OrderedModel.objects.all()
self.assertEqual(juan[1], 1)
self.assertEqual(juan[2], 2)
self.assertEqual(pepe[1], 1)
self.assertEqual(pepe[5], 2)
    """
    nodes = parse(code)
    assert not is_flaky(nodes)
