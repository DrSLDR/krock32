# krock32

_A base32 decoder/encoder using Crockford's alphabet, v0.0.1_

krock32 is a Python implementation of [Crockford's base32 alphabet](https://www.crockford.com/base32.html), including checksumming. It is created to allow encoding of arbitrary data to a human readable format, allowing for human-to-human transmission, while also being machine-decodable. All this without being case-sensitive or using special characters like base64 does.

## Base32?

Base32 is the encoding of arbitrary data into a set of 32 (human-readable) symbols, which make up the encoding's alphabet. In most implementations, this allows any data to be represented entirely as ASCII characters, which is useful for certain forms of transmission. In difference from the more common base64, which uses 64 symbols, base32 can be case-insensitive and exclude special, non-alphanumeric characters.

Encoding data to base32 will, necessarily, expand the data. A byte of data can encode 256 values (8 bits), whereas a symbol of base32 can only encode 32 values (5 bits). This means the base32-encoded data will be 60% larger (8/5) than the base data. The shortest example is that 5 bytes (40 bits) will encode to 8 base32 symbols.

Crockford's base32 alphabet differs from the [RFC 4648](https://tools.ietf.org/html/rfc4648#section-6) standard in n ways:

1. It starts with the numerals, so that e.g. `0b00001` encodes to `1`.
2. It does not use padding, so encodings of data not divisible by 5 bytes will not be padded with `=`.
3. It explicitly defines that both upper and lowercase characters are valid to the decoder, so that e.g. both `G` and `g` decode to `0b10000`.
4. It eliminates commonly mis-read characters `I`, `L`, `O`, and `U` from the encoding. Instead, `O`, `o`, and `0` all decode to `0b00000` and `1`, `I`, `i`, `L`, and `l` all decode to `0b00001`. `U` and `u` are only used as checksums.
5. It optionally allows a checksum to be appended to the very end of the encoded data.

## Is it any good?

[yes.](https://news.ycombinator.com/item?id=3067434)

