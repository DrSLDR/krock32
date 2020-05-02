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

class TestEncoder:
    def test_instatiates(self):
        assert isinstance(Z.Encoder(), Z.Encoder)

    def test_alphabet(self):
        ec = Z.Encoder()
        alphabet = {
            0: 'y',
            1: 'b',
            2: 'n',
            3: 'd',
            4: 'r',
            5: 'f',
            6: 'g',
            7: '8',
            8: 'e',
            9: 'j',
            10: 'k',
            11: 'm',
            12: 'c',
            13: 'p',
            14: 'q',
            15: 'x',
            16: 'o',
            17: 't',
            18: '1',
            19: 'u',
            20: 'w',
            21: 'i',
            22: 's',
            23: 'z',
            24: 'a',
            25: '3',
            26: '4',
            27: '5',
            28: 'h',
            29: '7',
            30: '6',
            31: '9'
        }
        assert ec._alphabet == alphabet

    def _get_encoding_set(self):
        return [
            ([0x27], 'rh======'),
            ([0xb7], 'sh======'),
            ([0xc6], 'aa======'),
            ([0xb7,0xc6], 's9my====')
        ]

    def test_simple_encodings(self):
        for bts, encoding in self._get_encoding_set():
            ec = Z.Encoder()
            ec.update(bts)
            assert ec.finalize() == encoding

    def test_update_after_final(self):
        ec = Z.Encoder()
        ec.update(0)
        ec.finalize()
        with pytest.raises(Z.EncoderAlreadyFinalizedException):
            ec.update(0)
