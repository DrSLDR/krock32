# decode.py

"""
Krock32 Decoder

Class definition for the Krock32 decoder, taking a Crockford Base32 string
and turning it into bytes-data.
"""

from collections import namedtuple


class DecoderAlreadyFinalizedException(Exception):
    pass


class Decoder:
    def __init__(self, strict=False, ignore_non_alphabet=True):
        self._string_buffer: str = ''
        self._bytearray: bytearray = bytearray()
        self._strict: bool = strict
        self._ignore_non_alphabet: bool = ignore_non_alphabet
        self._alphabet = self._make_alphabet(
            '0123456789ABCDEFGHJKMNPQRSTVWXYZ*~$=U',
            strict=self._strict
        )
        self._is_finished = False
        self._p_sym = namedtuple('ProcessedSymbol', ['byte', 'rem'])

    def _make_alphabet(self, alphabet_string: str, strict: bool) -> dict:
        alphabet = {}
        for i, x in enumerate(alphabet_string):
            alphabet[x.upper()] = i
            if not strict:
                alphabet[x.lower()] = i
        if not strict:
            alphabet['O'], alphabet['o'] = 0, 0
            (alphabet['I'], alphabet['i'],
             alphabet['L'], alphabet['l']) = 1, 1, 1, 1
        return alphabet

    def _decode_first_symbol(self, symbol: str) -> bytes:
        return self._p_sym(byte=self._alphabet.get(symbol), rem=0)

    def _decode_quantum(self, quantum: str) -> bytearray:
        buffer = bytearray()
        p_sym = self._decode_first_symbol(quantum[0])
        if len(quantum) == 1:
            return buffer.append(p_sym.byte << 3)

    def _consume(self):
        while len(self._string_buffer) > 8:
            quantum: str = self._string_buffer[0:8]
            self._string_buffer = self._string_buffer[8:]
            self._bytearray.extend(self._decode_quantum(quantum))

    def update(self, string: str):
        if self._is_finished:
            raise DecoderAlreadyFinalizedException
        self._string_buffer += string
        self._consume()

    def finalize(self) -> bytes:
        if self._is_finished:
            raise DecoderAlreadyFinalizedException
        self._is_finished = True
        self._bytearray.extend(
            self._decode_quantum(self._string_buffer)
            if len(self._string_buffer) > 0 else [])
        return bytes(self._bytearray)
