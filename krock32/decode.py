# decode.py

"""
Krock32 Decoder

Class definition for the Krock32 decoder, taking a Crockford Base32 string
and turning it into bytes-data.
"""


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
