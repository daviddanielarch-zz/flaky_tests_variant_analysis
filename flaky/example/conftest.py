import os
import traceback

import django.template.defaultfilters
import pytest
from django.db.models import QuerySet


def custom_getitem(self, k):
    if isinstance(k, int) and not self.ordered:

        call_stack = traceback.extract_stack()

        caller_filename = os.path.basename(call_stack[-2].filename)

        if caller_filename.startswith('test_'):
            data.add(k)

    return django.db.models.query.QuerySet.original_getitem(self, k)


@pytest.yield_fixture(autouse=True)
def flaky_detect(monkeypatch):
    global data
    data = set()

    django.db.models.query.QuerySet.original_getitem = django.db.models.query.QuerySet.__getitem__
    monkeypatch.setattr(django.db.models.query.QuerySet, '__getitem__', custom_getitem)

    yield

    if len(data) >= 2:
        raise Exception('Possible flaky test detected.')
