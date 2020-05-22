# krock32

_A base32 decoder/encoder using Crockford's alphabet, v0.1.0_

krock32 is a Python implementation of [Crockford's base32 alphabet](https://www.crockford.com/base32.html), including checksumming. It is created to allow encoding of arbitrary data to a human readable format, allowing for human-to-human transmission, while also being machine-decodable. All this without being case-sensitive or using special characters like base64 does.

## Base32?

Base32 is the encoding of arbitrary data into a set of 32 (human-readable) symbols, which make up the encoding's alphabet. In most implementations, this allows any data to be represented entirely as ASCII characters, which is useful for certain forms of transmission. In difference from the more common base64, which uses 64 symbols, base32 can be case-insensitive and exclude special, non-alphanumeric characters.

Encoding data to base32 will, necessarily, expand the data. A byte of data can encode 256 values (8 bits), whereas a symbol of base32 can only encode 32 values (5 bits). This means the base32-encoded data will be 60% larger (8/5) than the base data. The shortest example is that 5 bytes (40 bits) will encode to 8 base32 symbols.

Crockford's base32 alphabet differs from the [RFC 4648](https://tools.ietf.org/html/rfc4648#section-6) standard in 5 ways:

1. It starts with the numerals, so that e.g. `0b00001` encodes to `1`.
2. It does not use padding, so encodings of data not divisible by 5 bytes will not be padded with `=`. Instead, the missing bits are treated as zeros and a last symbol is selected from that.
3. It explicitly defines that both upper and lowercase characters are valid to the decoder, so that e.g. both `G` and `g` decode to `0b10000`.
4. It eliminates commonly mis-read characters `I`, `L`, `O`, and `U` from the encoding. Instead, `O`, `o`, and `0` all decode to `0b00000` and `1`, `I`, `i`, `L`, and `l` all decode to `0b00001`. `U` and `u` are only used as checksums.
5. It optionally allows a checksum to be appended to the very end of the encoded data.

## Installation

You should be able to install krock32 from [PyPi](https://pypi.org):

```shell
pip install krock32
```

I have only ever tested it for Python 3.8, but I see no reason it shouldn't work for earlier 3.x versions. 2.7 is not supported, but may work, what do I know.

### Testing

There's a test suite in `tests/test_krock32.py` which requires [`pytest`](https://pypi.org/project/pytest/) and [`hypothesis`](https://pypi.org/project/hypothesis/) to run. Given those prerequisites, testing should be as easy as

```shell
cd tests
pytest
```

## Usage

krock32 is relatively easy to use. There are two objects - `Encoder` and `Decoder` - that have two methods - `update()` and `finalize()`.

### Encoder

The encoder takes bytes-like data (`bytes` or `bytearray`) and encodes into Crockford base32.

```python
import krock32

encoder = krock32.Encoder(checksum=True)
# Instantiates a krock32 encoder, here with the optional checksum enabled.
# If checksum is not given, it is False by default.

encoder.update(b'this is some bytes data')
# Calling update feeds data into the encoder, updating its internal state.
encoder.update(b'this is more, fun data')
# Consecutive updates are allowed; this just appends the new data

encoding = encoder.finalize()
# Calling finalize returns the encoded string from the encoder. It also
# disables the encoder, so to encode more data you must instantiate a
# new encoder.

# In the code above, encoding is:
# EHM6JWS0D5SJ0WVFDNJJ0RKSEHJQ6834C5T62X38D5SJ0TBK41PPYWK55GG6CXBE41J62X31W
# where the final 'W' is the checksum.

```

### Decoder

The inverse of the encoder, the decoder takes a Crockford base32 string and decodes it into `bytes`.

```python
import krock32

decoder = krock32.Decoder(strict=False, checksum=True)
# Instantiates a krock32 decoder, here with the optional checksum enabled
# and strictness - allowing only the 32 symbols generated by the encoder -
# disabled. Note that if a string is encoded with a checksum, the decoder
# must also have checksumming enabled, and vice versa.
# If checksum is not given, it is False by default.
# Note: There is a third option: ignore_non_alphabet. It is currently
# not implemented, but will allow filtering out all symbols not in the
# alphabet, such as whitespace and unicode garbage.

decoder.update('EHM6JWS0D5SJ0WVFDNJJ0RKSEHJQ6834')
# Calling update feeds data into the decoder, updating its internal state.
decoder.update('c5t62x38d5sj0tbk41ppywk55gg6cxbe41j62x31w')
# Consecutive updates are allowed; this just appends the new data

# Even though the input string's length must be a multiple of 8 symbols plus
# 0, 2, 4, 5, or 7 (1, 3, 5, or 6 with checksumming), each call to update can
# be of any length.

decoding = decoder.finalize()
# Calling finalize returns the decoded bytes from the decoder. It also
# disables the decoder, so to decode more data you must instantiate a
# new decoder.

# In the code above, decoding is:
# b'this is some bytes datathis is more, fun data'
```

## License and acknowlegements

krock32 is licensed under the [MIT license](https://github.com/DrSLDR/krock32/blob/master/LICENSE).

krock32 implements Douglas Crockford's ([@douglascrockford](https://github.com/douglascrockford)) [base32 alphabet and checksumming scheme](https://www.crockford.com/base32.html) with his permission.

## Changelog

- **0.1.0** Initial release.
- **0.1.0** Development version. This project started out named `zim` and implemented [z-base-32](https://www.wikiwand.com/en/Base32#/z-base-32). This was later discarded when I learned that Crockford's alphabet does a better job with interchangeable symbols, which I explicitly wanted. Package changed its name to `krock32`.

## Is it any good?

[yes.](https://news.ycombinator.com/item?id=3067434)

