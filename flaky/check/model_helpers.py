from check.ast_helpers import get_model_queryset, logger
from example.models import TheModel, OrderedModel


def is_model_queryset_call(node):
    """
    Check if the given node is queryset call over a model and if it might be vulnerable.

    The criteria to check if its a queryset call is:
        * The object is a model (if we can't check that its a mode a warning will be printed)
        * One of the attributes on the call is 'objects'

    Criteria for vulnerability is:
        * Does not have an ordering Meta field
        * Is not calling order_by
    """
    model_name, method_calls = get_model_queryset(node)
    if not method_calls:
        return False

    return ('objects' in method_calls and
            'order_by' not in method_calls and
            'create' not in method_calls and
            'get' not in method_calls and
            is_django_model_vulnerable(model_name)
            )


def is_django_model_vulnerable(model_name):
    """This is a dinamic check, if model_name is not a model, we will assume it is"""
    try:
        obj = eval(model_name)
        is_vulnerable = is_django_model(obj) and not has_django_model_ordering(obj)

    except NameError:
        is_vulnerable = True
        #logger.warning('Found queryset call with {}, but the model was not imported'.format(model_name))

    return is_vulnerable


def has_django_model_ordering(model):
    """
    Check if the given model has ordering
    """
    return model._meta.ordering


def is_django_model(model):
    """
    Check if the given object is a django Model
    """
    return model.__class__.__name__ == 'ModelBase'
