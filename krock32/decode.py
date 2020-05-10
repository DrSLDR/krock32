# decode.py

"""
Krock32 Decoder

Class definition for the Krock32 decoder, taking a Crockford Base32 string
and turning it into bytes-data.
"""

class Decoder:
    def __init__(self, permissive=False, ignore_non_alphabet=True):
        self._string_buffer: str = ''
        self._bytearray: bytearray = bytearray()
        self._permissive: bool = permissive
        self._ignore_non_alphabet: bool = ignore_non_alphabet
        self._alphabet = self._make_alphabet(
            'ybndrfg8ejkmcpqxot1uwisza345h769',
            permissive=self._permissive
        )

    def _make_alphabet(self, alphabet_string:str, permissive: bool) -> dict:
        alphabet = {}
        for i, x in enumerate(alphabet_string):
            alphabet[x.lower()] = i
            alphabet[x.upper()] = i
        if permissive:
            # Inject doubles for easier, more permissive parsing
            alphabet['0'] = 16 # means o, O, 0 decodes to 16
            alphabet['l'] = 18
            alphabet['L'] = 18 # means 1, l, L decodes to 18
            # i and I are also doubles of 1, but let's assume they can be
            # read properly
        return alphabet
