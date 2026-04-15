"""Shared pytest config for the marathon exercise bank.

Pytest's default import mode prepends each test file's parent directory
to sys.path when there's no __init__.py, so `from problem import X`
works automatically inside each exercise directory. We only add a
deterministic random seed fixture here.
"""

from __future__ import annotations

import random

import pytest


@pytest.fixture(autouse=True)
def _deterministic_seed():
    random.seed(42)
    yield
