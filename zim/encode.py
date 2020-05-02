# encode.py

"""
Zim encoder

Class definition for the zim encoder, taking bytes-data and turning it into
z-base-32 string.
"""

class EncoderAlreadyFinalizedException(Exception):
    pass


class Encoder():
    def __init__(self):
        self._string = ''
        self._byte_buffer = bytearray()
        self._alphabet = self._make_alphabet(
            'ybndrfg8ejkmcpqxot1uwisza345h769'
        )
        self._is_finished = False

    def _make_alphabet(self, alphabet_string: str) -> dict:
        alphabet = {}
        for i, x in enumerate(alphabet_string):
            alphabet[i] = x
        return alphabet

    def _render_quantum(self, quantum: bytearray) -> str:
        the_string = ''
        data_byte = quantum[0]
        quint = data_byte >> 3
        remainder = (data_byte & 0b111) << 2
        the_string += self._alphabet.get(quint)
        if len(quantum) == 1:
            the_string += self._alphabet.get(remainder)
            the_string += '======'
            return the_string

    def _consume(self):
        while len(self._byte_buffer) > 5:
            quantum = self._byte_buffer[0:5]
            del self._byte_buffer[0:5]
            self._string += self._render_quantum(quantum)

    def update(self, data: bytes):
        if self._is_finished:
            raise EncoderAlreadyFinalizedException
        self._byte_buffer.extend(bytearray(data))
        self._consume()

    def finalize(self) -> str:
        self._is_finished = True
        return self._string + self._render_quantum(self._byte_buffer)
