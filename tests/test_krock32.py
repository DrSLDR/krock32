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


def _get_encoding_set():
    return [
        ([], '', '0'),
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


def _get_encoded_text_strategy(length=8, strict=True):
    if strict:
        alphabet = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
    else:
        alphabet = ('0123456789ABCDEFGHJKMNPQRSTVWXYZ'
                    'abcdefghjkmnpqrstvwxyzOoIiLl')
    return st.text(alphabet=alphabet, min_size=length, max_size=length)


@st.composite
def _get_encoded_stub_text_strategy(draw, length, strict=True):
    setA = set('0G')
    setB = set('8R')
    setC = set('4CMW')
    setD = set('26AEJPTY')
    if not strict:
        setA |= set('Oog')
        setB |= set('r')
        setC |= set('cmw')
        setD |= set('aejpty')
    if length == 2:
        b = draw(_get_encoded_text_strategy(length=1, strict=strict))
        s = draw(st.text(alphabet=(setA | setB | setC), min_size=1,
                 max_size=1))
    elif length == 4:
        b = draw(_get_encoded_text_strategy(length=3, strict=strict))
        s = draw(st.text(alphabet=(setA), min_size=1, max_size=1))
    elif length == 5:
        b = draw(_get_encoded_text_strategy(length=4, strict=strict))
        s = draw(st.text(alphabet=(setA | setB | setC | setD), min_size=1,
                 max_size=1))
    elif length == 7:
        b = draw(_get_encoded_text_strategy(length=6, strict=strict))
        s = draw(st.text(alphabet=(setA | setB), min_size=1, max_size=1))
    else:
        return ''
    return ''.join([b, s])


@st.composite
def _get_encoded_complex_text_strategy(draw, strict=True):
    base = draw(st.lists(_get_encoded_text_strategy(strict=strict)))
    stub_length = draw(st.integers(min_value=2, max_value=7))
    stub = draw(_get_encoded_stub_text_strategy(length=stub_length,
                                                strict=strict))
    return ''.join([''.join(base), stub])


class TestEncoder:
    def test_instantiates(self):
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

    def test_simple_encodings(self):
        for bts, encoding, _ in _get_encoding_set():
            ec = K.Encoder()
            ec.update(bts)
            assert ec.finalize() == encoding

    def test_checksum_encodings(self):
        for bts, encoding, cs in _get_encoding_set():
            ec = K.Encoder(checksum=True)
            ec.update(bts)
            ret = ec.finalize()
            assert ret[:-1] == encoding
            assert ret[-1] == cs

    @given(b=st.binary())
    def test_any_simple_encode(self, b):
        ec = K.Encoder()
        ec.update(b)
        assert ec.finalize() is not None

    @given(bs=st.lists(st.binary()))
    def test_any_complex_encode(self, bs):
        ec = K.Encoder()
        for b in bs:
            ec.update(b)
        assert ec.finalize() is not None

    @given(b=st.binary())
    def test_any_simple_encode_with_checksum(self, b):
        ec = K.Encoder(checksum=True)
        ec.update(b)
        cs = 0
        for byte in b:
            cs = cs << 8
            cs += byte
        cs = cs % 37
        v = ec.finalize()
        assert v is not None
        assert v[-1] == ec._alphabet.get(cs)

    @given(bs=st.lists(st.binary()))
    def test_any_complex_encode_with_checksum(self, bs):
        ec = K.Encoder(checksum=True)
        cs = 0
        for b in bs:
            ec.update(b)
            for byte in b:
                cs = cs << 8
                cs += byte
        cs = cs % 37
        v = ec.finalize()
        assert v is not None
        assert v[-1] == ec._alphabet.get(cs)

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
    def test_instantiates(self):
        assert isinstance(K.Decoder(), K.Decoder)

    def test_alphabet_permissive(self):
        ec = K.Decoder()
        alphabet = {
            '0': 0, 'O': 0, 'o': 0,
            '1': 1, 'I': 1, 'i': 1, 'L': 1, 'l': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'A': 10, 'a': 10,
            'B': 11, 'b': 11,
            'C': 12, 'c': 12,
            'D': 13, 'd': 13,
            'E': 14, 'e': 14,
            'F': 15, 'f': 15,
            'G': 16, 'g': 16,
            'H': 17, 'h': 17,
            'J': 18, 'j': 18,
            'K': 19, 'k': 19,
            'M': 20, 'm': 20,
            'N': 21, 'n': 21,
            'P': 22, 'p': 22,
            'Q': 23, 'q': 23,
            'R': 24, 'r': 24,
            'S': 25, 's': 25,
            'T': 26, 't': 26,
            'V': 27, 'v': 27,
            'W': 28, 'w': 28,
            'X': 29, 'x': 29,
            'Y': 30, 'y': 30,
            'Z': 31, 'z': 31,
            # Extended checksum values
            '*': 32,
            '~': 33,
            '$': 34,
            '=': 35,
            'U': 36, 'u': 36
        }
        assert ec._alphabet == alphabet

    def test_alphabet_strict(self):
        ec = K.Decoder(strict=True)
        alphabet = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'A': 10,
            'B': 11,
            'C': 12,
            'D': 13,
            'E': 14,
            'F': 15,
            'G': 16,
            'H': 17,
            'J': 18,
            'K': 19,
            'M': 20,
            'N': 21,
            'P': 22,
            'Q': 23,
            'R': 24,
            'S': 25,
            'T': 26,
            'V': 27,
            'W': 28,
            'X': 29,
            'Y': 30,
            'Z': 31,
            # Extended checksum values
            '*': 32,
            '~': 33,
            '$': 34,
            '=': 35,
            'U': 36
        }
        assert ec._alphabet == alphabet

    def test_simple_decodings(self):
        for bts, encoding, _ in _get_encoding_set():
            dc = K.Decoder()
            dc.update(encoding)
            assert dc.finalize() == bytes(bts)

    def test_simple_decodings_fuzzed(self):
        ec = K.Encoder()
        for bts, encoding, _ in _get_encoding_set():
            if len(encoding) == 8:
                continue
            for fuzz in range(32):
                if fuzz & (pow(2, [
                        0, 0, 2, 0, 4, 1, 0, 3][len(encoding) % 8]) - 1) == 0:
                    continue
                fuzzc = ec._alphabet.get(fuzz)
                encoding = encoding[:-1] + fuzzc
                dc = K.Decoder()
                dc.update(encoding)
                with pytest.raises(K.decode.DecoderNonZeroCarryException):
                    dc.finalize()

    def test_checksum_decodings(self):
        for bts, encoding, cs in _get_encoding_set():
            dc = K.Decoder(checksum=True)
            dc.update(encoding)
            dc.update(cs)
            assert dc.finalize() == bytes(bts)

    def test_bad_checksum_decodings(self):
        ec = K.Encoder()
        for bts, encoding, cs in _get_encoding_set():
            for bcs in ec._alphabet.values():
                if bcs == cs:
                    continue
                dc = K.Decoder(checksum=True)
                dc.update(encoding)
                dc.update(bcs)
                with pytest.raises(K.decode.DecoderChecksumException):
                    dc.finalize()

    @given(t=_get_encoded_complex_text_strategy())
    def test_any_simple_strict_decode(self, t):
        dc = K.Decoder()
        dc.update(t)
        assert dc.finalize() is not None

    @given(t=_get_encoded_complex_text_strategy(strict=False))
    def test_any_simple_decode(self, t):
        dc = K.Decoder()
        dc.update(t)
        assert dc.finalize() is not None

    def test_update_after_final(self):
        ec = K.Decoder()
        ec.update('')
        ec.finalize()
        with pytest.raises(K.decode.DecoderAlreadyFinalizedException):
            ec.update('')

    def test_multiple_final(self):
        ec = K.Decoder()
        ec.update('')
        ec.finalize()
        with pytest.raises(K.decode.DecoderAlreadyFinalizedException):
            ec.finalize()


class TestEncodeAndDecode:
    @given(b=st.binary())
    def test_encode_decode_encode_equal(self, b):
        ec = K.Encoder()
        dc = K.Decoder()
        ec.update(b)
        dc.update(ec.finalize())
        assert b == dc.finalize()

    @given(b=st.binary())
    def test_encode_decode_encode_with_checksum_equal(self, b):
        ec = K.Encoder(checksum=True)
        dc = K.Decoder(checksum=True)
        ec.update(b)
        dc.update(ec.finalize())
        assert b == dc.finalize()

    @given(t=_get_encoded_complex_text_strategy())
    def test_decode_encode_decode_equal(self, t):
        ec = K.Encoder()
        dc = K.Decoder()
        dc.update(t)
        ec.update(dc.finalize())
        assert t == ec.finalize()

    @given(ts=st.lists(_get_encoded_text_strategy()))
    def test_long_decode_encode_decode_equal(self, ts):
        ec = K.Encoder()
        dc = K.Decoder()
        for t in ts:
            dc.update(t)
        ec.update(dc.finalize())
        assert ''.join(ts) == ec.finalize()
