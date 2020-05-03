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
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'A',
            11: 'B',
            12: 'C',
            13: 'D',
            14: 'E',
            15: 'F',
            16: 'G',
            17: 'H',
            18: 'J',
            19: 'K',
            20: 'M',
            21: 'N',
            22: 'P',
            23: 'Q',
            24: 'R',
            25: 'S',
            26: 'T',
            27: 'V',
            28: 'W',
            29: 'X',
            30: 'Y',
            31: 'Z'
        }
        assert ec._alphabet == alphabet

    def _get_encoding_set(self):
        return [
            ([0x27], '4W'),
            ([0xb7], 'PW'),
            ([0xc6], 'RR'),
            ([0xfe], 'ZR'),
            ([0x7e], 'FR'),
            ([0x46], '8R'),
            ([0x27, 0xb7], '4YVG'),
            ([0xb7, 0xc6], 'PZ30'),
            ([0xc6, 0xfe], 'RVZ0'),
            ([0xfe, 0x7e], 'ZSZ0'),
            ([0x7e, 0x46], 'FS30'),
            ([0x27, 0xb7, 0xc6], '4YVWC'),
            ([0xb7, 0xc6, 0xfe], 'PZ3FW'),
            ([0xc6, 0xfe, 0x7e], 'RVZ7W'),
            ([0xfe, 0x7e, 0x46], 'ZSZ4C'),
            ([0x27, 0xb7, 0xc6, 0xfe], '4YVWDZG'),
            ([0xb7, 0xc6, 0xfe, 0x7e], 'PZ3FWZG'),
            ([0xc6, 0xfe, 0x7e, 0x46], 'RVZ7WHG'),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e], '4YVWDZKY'),
            ([0xb7, 0xc6, 0xfe, 0x7e, 0x46], 'PZ3FWZJ6'),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e, 0x46], '4YVWDZKY8R')
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
