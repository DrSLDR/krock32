# test_zim.py

"""
Testsuite for Zim
"""

from hypothesis import given
import hypothesis.strategies as st
import os
import pytest
import sys

sys.path[0] = os.path.dirname(sys.path[0])

import zim as Z

class TestEncoder():
    def test_instatiates(self):
        assert isinstance(Z.Encoder(), Z.Encoder)
