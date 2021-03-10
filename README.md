# Encoders
A simple encoding program with a personal encoding and simple base64 encodings


Download both files and run the encoding.py for the gui, or just use the begin() function of encodelib.py to do it yourself - I still need to add docstrings

# How begin() works:
The first argument is the string to encode.
The second one is a string of options, comprised of the following: 'e' (encode), 'd' (decode), 'c' (complex mode), and 'b' (base64 mode). These are evaluated in the same was as open() evaluates its options, raising ValueError if incorrect option combinations are specified (and telling you what you did wrong).
