"""Shared pytest config for the marathon exercise bank.

Pytest's default import mode prepends each test file's parent directory
to sys.path when there's no __init__.py, so `from problem import X`
works automatically inside each exercise directory. We only add a
deterministic random seed fixture and incremental test support here.
"""

from __future__ import annotations

import random

import pytest


@pytest.fixture(autouse=True)
def _deterministic_seed():
    random.seed(42)
    yield


# --- Incremental test support ---
# Mark a test class with @pytest.mark.incremental to skip remaining
# tests after the first failure. This gives a "one error at a time"
# UX inspired by python_koans and rustlings.


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"previous test failed ({previousfailed.name})")
