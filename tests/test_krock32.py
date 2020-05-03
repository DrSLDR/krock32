# test_zim.py

"""
Testsuite for Krock32
"""

from hypothesis import given
import hypothesis.strategies as st
import os
import pytest
import sys

sys.path[0] = os.path.dirname(sys.path[0])

import krock32 as K

class TestEncoder:
    def test_instatiates(self):
        assert isinstance(K.Encoder(), K.Encoder)

    def test_alphabet(self):
        ec = K.Encoder()
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
            ([0xfe], '9a======'),
            ([0x7e], 'xa======'),
            ([0x46], 'ea======'),
            ([0x27, 0xb7], 'r65o===='),
            ([0xb7, 0xc6], 's9dy===='),
            ([0xc6, 0xfe], 'a59y===='),
            ([0xfe, 0x7e], '939y===='),
            ([0x7e, 0x46], 'x3dy===='),
            ([0x27, 0xb7, 0xc6], 'r65hc==='),
            ([0xb7, 0xc6, 0xfe], 's9dxh==='),
            ([0xc6, 0xfe, 0x7e], 'a598h==='),
            ([0xfe, 0x7e, 0x46], '939rc==='),
            ([0x27, 0xb7, 0xc6, 0xfe], 'r65hp9o=='),
            ([0xb7, 0xc6, 0xfe, 0x7e], 's9dxh9o=='),
            ([0xc6, 0xfe, 0x7e, 0x46], 'a598hto=='),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e], 'r65hp9u6'),
            ([0xb7, 0xc6, 0xfe, 0x7e, 0x46], 's9dxh91g'),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e, 0x46], 'r65hp9u6ea======')
        ]

    def test_simple_encodings(self):
        for bts, encoding in self._get_encoding_set():
            ec = K.Encoder()
            ec.update(bts)
            assert ec.finalize() == encoding

    def test_update_after_final(self):
        ec = K.Encoder()
        ec.update([0])
        ec.finalize()
        with pytest.raises(K.EncoderAlreadyFinalizedException):
            ec.update([0])


class TestDecoder:
    def test_instatiates(self):
        assert isinstance(K.Decoder(), K.Decoder)
