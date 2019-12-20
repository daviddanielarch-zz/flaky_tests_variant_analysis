from ast import parse

from ..analyze import is_assert_equal


def test_is_assert_equal():
    node = parse('self.assertEqual(1, 2)').body[0]
    assert is_assert_equal(node)


def test_invalid_node_type():
    node = parse('num = 1').body[0]
    assert not is_assert_equal(node)


def test_is_not_assert_equal():
    node = parse('self.assertRaises(1)').body[0]
    assert not is_assert_equal(node)
