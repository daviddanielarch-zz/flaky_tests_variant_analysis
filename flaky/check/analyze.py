import ast
import logging

from collections import defaultdict

from check.ast_helpers import (
    is_assert_equal,
    has_numeric_subscript,
    get_subscript,
    get_numeric_subscript_variable_name_and_index,
    get_variable_full_name)

from check.model_helpers import is_model_queryset_call


logger = logging.getLogger()


class Analyzer(ast.NodeVisitor):
    def __init__(self, filepath):
        self.filepath = filepath

    def visit_FunctionDef(self, node):
        if is_flaky(node):
            print('Found flaky test: {} ({})'.format(node.name, self.filepath))

        self.generic_visit(node)


def is_flaky(node):
    variable_names = set()
    variable_usage_indexes = defaultdict(list)

    for child in node.body:
        if isinstance(child, ast.Assign):
            if is_model_queryset_call(child.value):
                for target in child.targets:
                    variable_names.add(get_variable_full_name(target))

        if is_assert_equal(child):
            args = child.value.args
            for arg in args:
                if has_numeric_subscript(arg):
                    subscript = get_subscript(arg)
                    name, index = get_numeric_subscript_variable_name_and_index(subscript)

                    if name in variable_names:
                        variable_usage_indexes[name].append(index)

    return any([len(set(usages)) >= 2 for usages in variable_usage_indexes.values()])


def find_flaky_from_file(filepath):
    with open(filepath, "r") as source:
        try:
            tree = ast.parse(source.read())
        except UnicodeDecodeError:
            return

    analyzer = Analyzer(filepath)
    analyzer.visit(tree)
