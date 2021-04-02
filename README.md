# Encoders
A simple encoding program with a personal encoding and simple base64 encodings


Download both files and run the encoding.py for the gui, or just use the `begin()` function of `encodelib.py` to do it yourself - I still need to add docstrings

# How begin() works:
The first argument is the string to encode.
The second one is a string of options, comprised of the following: 'e' (encode), 'd' (decode), 'c' (complex mode), and 'b' (base64 mode). These are evaluated in the same was as open() evaluates its options, raising ValueError if incorrect option combinations are specified (and telling you what you did wrong).
If you specified a complex encoding, you will get a tuple consisting of: `The encoded string, the shuffled list, the shuffled lists shuffle key, and the general key.` Then, all you need to do is pass them into the complex decoding at the other end as a non-positional argument.
If you specified a normal encoding, you will get a tuple that consists of the encoded message, and the key: again just pass them into the `begin()` statement.
Finally, when encoding, the `encode_special_characters` bool will just be passed straight through to the encoding; this makes it so characters that are not letters or numbers do not get encoded. This includes spaces. WARNING: Support has yet to be added to decode this.
