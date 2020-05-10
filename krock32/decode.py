# decode.py

"""
Krock32 Decoder

Class definition for the Krock32 decoder, taking a Crockford Base32 string
and turning it into bytes-data.
"""

from collections import namedtuple


class DecoderAlreadyFinalizedException(Exception):
    pass


class DecoderInvalidStringLengthException(Exception):
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
        self._p_byte = namedtuple('ProcessedByte', ['byte', 'carry'])

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

    def _decode_first_byte(self, symbols: str) -> tuple:
        byte = self._alphabet.get(symbols[0]) << 3
        second_sym = self._alphabet.get(symbols[1])
        byte += second_sym >> 2
        carry = second_sym & 0b11
        return self._p_byte(byte=byte, carry=carry)

    def _decode_quantum(self, quantum: str) -> bytearray:
        if not len(quantum) in [2, 4, 5, 7, 8]:
            raise DecoderInvalidStringLengthException
        buffer = bytearray()
        p_byte = self._decode_first_byte(quantum[0:2])
        buffer.append(p_byte.byte)
        if len(quantum) == 2:
            if p_byte.carry == 0:
                return buffer
            else:
                # Handle illegal bytes; carry must be zero for this string
                # to make sense
                pass

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
