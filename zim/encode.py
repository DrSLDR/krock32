# encode.py

"""
Zim encoder

Class definition for the zim encoder, taking bytes-data and turning it into
z-base-32 string.
"""

from collections import namedtuple

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
        self._p_quin = namedtuple('ProcessedQuin', ['sym', 'rem'])

    def _make_alphabet(self, alphabet_string: str) -> dict:
        alphabet = {}
        for i, x in enumerate(alphabet_string):
            alphabet[i] = x
        return alphabet

    def _render_first_quin(self, byte) -> tuple:
        quin = byte >> 3
        rem = (byte & 0b111) << 2
        return self._p_quin(sym=self._alphabet.get(quin),
                            rem=rem)

    def _render_second_quin(self, byte, remainder) -> tuple:
        sym = ''
        quin = (byte >> 6) + remainder
        sym += self._alphabet.get(quin)
        quin = (byte >> 1) & 0b11111
        rem = (byte & 0b1) << 4
        sym += self._alphabet.get(quin)
        return self._p_quin(sym=sym, rem=rem)

    def _render_quantum(self, quantum: bytearray) -> str:
        the_string = ''
        p_quin = self._render_first_quin(quantum[0])
        the_string += p_quin.sym
        if len(quantum) == 1:
            the_string += self._alphabet.get(p_quin.rem)
            the_string += '======'
            return the_string
        p_quin = self._render_second_quin(quantum[1], p_quin.rem)
        the_string += p_quin.sym
        if len(quantum) == 2:
            the_string += self._alphabet.get(p_quin.rem)
            the_string += '===='
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
