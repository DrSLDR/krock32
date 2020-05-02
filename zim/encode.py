# encode.py

"""
Zim encoder

Class definition for the zim encoder, taking bytes-data and turning it into
z-base-32 string.
"""


class Encoder():
    def __init__(self):
        self._string = ''
        self._byte_buffer = bytes(0)
        self._alphabet = self._make_alphabet(
            'ybndrfg8ejkmcpqxot1uwisza345h769'
        )

    def _make_alphabet(self, alphabet_string: str) -> dict:
        alphabet = {}
        for i, x in enumerate(alphabet_string):
            alphabet[i] = x
        return alphabet
