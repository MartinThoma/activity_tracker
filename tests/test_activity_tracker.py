#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `activity_tracker` package."""

# Third party modules
import pytest

# First party modules
import activity_tracker


def test_version() -> None:
    assert activity_tracker.__version__.count(".") == 2


def test_zero_division() -> None:
    with pytest.raises(ZeroDivisionError):
        1 / 0
