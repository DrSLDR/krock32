# decode.py

"""
Zim Decoder

Class definition for the zim decoder, taking a z-base-32 string and turning it
into bytes-data.
"""

class Decoder:
    def __init__(self, permissive=False, ignore_non_alphabet=True):
        self._string_buffer = ''
        self._bytearray = bytearray()
        self._permissive = permissive
        self._ignore_non_alphabet = ignore_non_alphabet