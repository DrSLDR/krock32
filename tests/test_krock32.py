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

# pylama:ignore=E402
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
            31: 'Z',
            # Extended checksum values
            32: '*',
            33: '~',
            34: '$',
            35: '=',
            36: 'U'
        }
        assert ec._alphabet == alphabet

    def _get_encoding_set(self):
        return [
            ([0x27], '4W', '2'),
            ([0xb7], 'PW', '='),
            ([0xc6], 'RR', 'D'),
            ([0xfe], 'ZR', '*'),
            ([0x7e], 'FR', 'F'),
            ([0x46], '8R', '~'),
            ([0x27, 0xb7], '4YVG', 'X'),
            ([0xb7, 0xc6], 'PZ30', 'K'),
            ([0xc6, 0xfe], 'RVZ0', 'Y'),
            ([0xfe, 0x7e], 'ZSZ0', 'Y'),
            ([0x7e, 0x46], 'FS30', 'S'),
            ([0x27, 0xb7, 0xc6], '4YVWC', '0'),
            ([0xb7, 0xc6, 0xfe], 'PZ3FW', 'C'),
            ([0xc6, 0xfe, 0x7e], 'RVZ7W', 'U'),
            ([0xfe, 0x7e, 0x46], 'ZSZ4C', 'H'),
            ([0x27, 0xb7, 0xc6, 0xfe], '4YVWDZG', '*'),
            ([0xb7, 0xc6, 0xfe, 0x7e], 'PZ3FWZG', 'G'),
            ([0xc6, 0xfe, 0x7e, 0x46], 'RVZ7WHG', 'U'),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e], '4YVWDZKY', 'Y'),
            ([0xb7, 0xc6, 0xfe, 0x7e, 0x46], 'PZ3FWZJ6', 'P'),
            ([0x27, 0xb7, 0xc6, 0xfe, 0x7e, 0x46], '4YVWDZKY8R', 'H')
        ]

    def test_simple_encodings(self):
        for bts, encoding, _ in self._get_encoding_set():
            ec = K.Encoder()
            ec.update(bts)
            assert ec.finalize() == encoding

    def test_checksum_encodings(self):
        for bts, encoding, cs in self._get_encoding_set():
            ec = K.Encoder(checksum=True)
            ec.update(bts)
            ret = ec.finalize()
            assert ret[:-1] == encoding
            assert ret[-1] == cs

    def test_update_after_final(self):
        ec = K.Encoder()
        ec.update([0])
        ec.finalize()
        with pytest.raises(K.encode.EncoderAlreadyFinalizedException):
            ec.update([0])

    def test_multiple_final(self):
        ec = K.Encoder()
        ec.update([0])
        ec.finalize()
        with pytest.raises(K.encode.EncoderAlreadyFinalizedException):
            ec.finalize()


class TestDecoder:
    def test_instatiates(self):
        assert isinstance(K.Decoder(), K.Decoder)
