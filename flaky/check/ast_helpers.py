import ast

import logging
logger = logging.getLogger()


def get_variable_full_name(node):
    names_list = get_variable_full_name_list(node)
    if names_list:
        return '.'.join(reversed(get_variable_full_name_list(node)))
    else:
        return ''


def get_variable_full_name_list(node):
    if isinstance(node, ast.Name):
        return [node.id]

    elif isinstance(node, ast.Attribute):
        if isinstance(node.value, ast.Name):
            return [node.attr, node.value.id]

        if isinstance(node.value, ast.Attribute):
            return [node.attr] + get_variable_full_name_list(node.value)
    else:
        return []


def is_assert_equal(node):
    """
    Test if the given node is an expression like:
    self.assertEqual(exp1, exp2)
    """
    if not isinstance(node, ast.Expr):
        return False

    call = node.value
    return (
            isinstance(call, ast.Call) and
            isinstance(call.func, ast.Attribute) and call.func.attr == 'assertEqual' and
            isinstance(call.func.value, ast.Name) and call.func.value.id == 'self'
    )


def get_subscript(node):
    """
    If there is a Subscript on the node, return it
    """
    if isinstance(node, ast.Attribute):
        return get_subscript(node.value)

    if isinstance(node, ast.Subscript):
        return node


def has_numeric_subscript(node):
    """
    Return if the node or one of its children is a Subscript with a numeric index

    node = models[0].name
    has_numeric_subscript(node) == True
    """
    if isinstance(node, ast.Attribute):
        return has_numeric_subscript(node.value)

    return (isinstance(node, ast.Subscript) and
            isinstance(node.slice, ast.Index) and
            isinstance(node.slice.value, ast.Num)
            )


def get_numeric_subscript_variable_name_and_index(node):
    """
    Return the variable name and the index for a Subscript with a numeric index

    node = 'pepe[0]'
    get_numeric_subscript_variable_name_and_index(node) == ('pepe', 0)
    """
    variable_name = get_variable_full_name(node.value)
    index = node.slice.value.n
    return variable_name, index


def get_model_queryset(node):
    """
    Return the model name and the call attributes for a given node

    node = Model.objects.all().filter().order_by()
    get_model_queryset(node) == 'Model', ['order_by', 'filter', 'all', 'objects']
    """
    names = get_names(node)
    if names:
        model, method_calls = names[-1], names[:-1]
    else:
        model, method_calls = 'None', []

    return model, set(method_calls)


def get_names(node):
    """
    Return all the attribute names for a model queryset call

    node = Model.objects.all().filter().order_by()
    get_names(node) == ['order_by', 'filter', 'all', 'objects', 'Model']
    """
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            return [node.func.attr] + get_names(node.func.value)
        elif isinstance(node.func, ast.Name):
            return [node.func.id]
        else:
            return []

    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return [node.attr, node.value.id]

    return []
