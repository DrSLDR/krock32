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
        self._string: str = ''
        self._byte_buffer: bytearray = bytearray()
        self._alphabet: dict = self._make_alphabet(
            'ybndrfg8ejkmcpqxot1uwisza345h769'
        )
        self._is_finished: bool = False
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

    def _render_third_quin(self, byte, remainder) -> tuple:
        quin = (byte >> 4) + remainder
        rem = (byte & 0b1111) << 1
        return self._p_quin(sym=self._alphabet.get(quin),
                            rem=rem)

    def _render_fourth_quin(self, byte, remainder) -> tuple:
        sym = ''
        quin = (byte >> 7) + remainder
        sym += self._alphabet.get(quin)
        quin = (byte >> 2) & 0b11111
        sym += self._alphabet.get(quin)
        rem = (byte & 0b11) << 3
        return self._p_quin(sym=sym, rem=rem)

    def _render_fifth_quin(self, byte, remainder) -> tuple:
        sym = ''
        quin = (byte >> 5) + remainder
        sym += self._alphabet.get(quin)
        quin = byte & 0b11111
        sym += self._alphabet.get(quin)
        return self._p_quin(sym=sym, rem=0)

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
        p_quin = self._render_third_quin(quantum[2], p_quin.rem)
        the_string += p_quin.sym
        if len(quantum) == 3:
            the_string += self._alphabet.get(p_quin.rem)
            the_string += '==='
            return the_string
        p_quin = self._render_fourth_quin(quantum[3], p_quin.rem)
        the_string += p_quin.sym
        if len(quantum) == 4:
            the_string += self._alphabet.get(p_quin.rem)
            the_string += '=='
            return the_string
        p_quin = self._render_fifth_quin(quantum[4], p_quin.rem)
        return the_string + p_quin.sym

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
