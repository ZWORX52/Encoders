import string
from base64 import b64encode as b64e, b64decode as b64d
from collections import deque
from random import randint as r, randrange as rr
from typing import Union


def _base64encode(s):
    return b64e(s.encode()).decode()


def _base64decode(s):
    return b64d(s.encode()).decode()


def _encode(s, max_char_len: int, encode_special_characters=True):
    encoded_return = ""
    for character in s:
        if encode_special_characters:
            encoded_return += _numbers_to_special_characters(str(ord(character)).zfill(max_char_len))
        else:
            if character in string.ascii_letters + string.digits:
                encoded_return += _numbers_to_special_characters(str(ord(character)).zfill(max_char_len))
            else:
                encoded_return += character
    return encoded_return


def _decode(s, max_char_len_: int):
    decoded_return = ""
    every_three = _split_into_list_of_len(s, max_char_len_)
    for characters in every_three:
        decoded_return += chr(_special_characters_to_numbers(characters))
    return decoded_return


def _encode2(s: str, max_char_len_: int):
    numbers_list = [ord(n) for n in s]
    rand_numbers_list = [r(1, 9) for _ in range(s.__len__())]
    shift_key = rr(0, 2 ** (s.__len__() // 2))
    shift_key_iter = bin(shift_key).lstrip("-0b").zfill(numbers_list.__len__() // 2)
    multiplied_numbers_list = []
    numbers_list_shuffled = _shuffle(shift_key_iter, rand_numbers_list)
    return_s = ""
    for n in range(len(numbers_list)):
        multiplied_numbers_list.append(str(numbers_list[n] * rand_numbers_list[n]).zfill(max_char_len_ + 1))
    for n in multiplied_numbers_list:
        return_s += _numbers_to_special_characters(n)
    return return_s, numbers_list_shuffled, shift_key, max_char_len_ + 1


def _decode2(s: str, max_char_len_: int, shuffled_list: list, shuffle_key_: int):
    return_string = ""
    special_char_list = [_special_characters_to_numbers(c) for c in _split_into_list_of_len(s, max_char_len_)]
    un_shuffled_list = _shuffle(bin(shuffle_key_).lstrip("-0b").zfill(shuffled_list.__len__() // 2), shuffled_list)
    number_list = [special_char_list[n] // un_shuffled_list[n] for n in range(special_char_list.__len__())]
    for char in number_list:
        return_string += chr(char)
    return return_string


def _numbers_to_special_characters(number):
    number_string = str(number)
    result = ""
    for character in number_string:
        result += numbers_to_special_characters_key[int(character)]
    return result


def _special_characters_to_numbers(characters: str):
    result = ""
    for character in characters:
        result += str(numbers_to_special_characters_key.index(character))
    return int(result)


def _test_input_yes_no(prompt: str, tries: int = 5, fail_message: str = "{} are not options, please try again! (Only "
                                                                        "yes, y, no, and n are acceptable") -> bool:
    if tries <= 0:
        raise ValueError("Can't try 0 or less times!")
    while True:
        all_tries = []
        for this_try in range(tries):
            last_answer = input(prompt).lower()
            if last_answer in ["y", "ye", "yes"]:
                return True
            elif last_answer in ["n", "no"]:
                return False
            all_tries.append(this_try)
        print(fail_message.format(all_tries))


def begin(s: str, types: str, /, shuffled_list: list = 0, shuffle_key: int = 0, key: int = 3, encode_special_characters:
          bool = True) -> Union[tuple[str, list, int, int], str]:
    encodings = _get_reps(types, ["e", "d", "c", "b"], ["encoding", "decoding", "complex", "base64"])
    if encodings[0] == "" and encodings[1] == "" and encodings[2] != "":
        raise ValueError("You need to specify one of either decode or encode with complex")
    elif encodings[0] == "" and encodings[1] == "" and encodings[3] != "":
        raise ValueError("You need to specify one of either decode or encode with base64")
    elif encodings[0] != "" and encodings[1] != "":
        raise ValueError("Cannot encode and decode at the same time")
    elif encodings[3] != "" and encodings[2] != "":
        raise ValueError("Can't be complex and base64 at the same time!")
    elif encodings[0] != "" and encodings[2] == "" and encodings[3] == "":
        return _encode(s, _get_max_char_len(s), encode_special_characters)
    elif encodings[0] != "" and encodings[2] != "":
        return _encode2(s, _get_max_char_len(s))
    elif encodings[0] != "" and encodings[3] != "":
        return _base64encode(s)
    elif encodings[1] != "" and encodings[2] == "":
        return _decode(s, key)
    elif encodings[1] != "" and encodings[2] != "":
        return _decode2(s, key, shuffled_list, shuffle_key)
    elif encodings[1] != "" and encodings[3] != "":
        return _base64decode(s)


def _split_into_list_of_len(_input: str, length: int):
    result = []
    __input = deque(_input)
    for character in range(len(__input) // length):
        this_every_three_append = ""
        for _ in range(length):
            this_every_three_append += __input.popleft()
        result.append(this_every_three_append)
    return result


def _get_max_char_len(s: str) -> int:
    return_int = 0
    for char in s:
        if str(ord(char)).__len__() > return_int:
            return_int = str(ord(char)).__len__()
    return return_int


def _shuffle(shift_key_iter, numbers_list):
    numbers_list_shuffled = []
    for n in range(len(shift_key_iter)):
        if shift_key_iter[n] == "1":
            numbers_list_shuffled.append(numbers_list[n * 2 + 1])
            numbers_list_shuffled.append(numbers_list[n * 2])
        else:
            numbers_list_shuffled.append(numbers_list[n * 2])
            numbers_list_shuffled.append(numbers_list[n * 2 + 1])
    if numbers_list.__len__() % 2 == 1:
        numbers_list_shuffled.append(numbers_list[-1])
    return numbers_list_shuffled


def _get_reps(s: str, reps: list[str], reps_keys: list[str]) -> list[str]:
    return_list = ["" for _ in range(len(reps))]
    if len(reps) != len(reps_keys):
        raise ValueError(f"reps needs to be the same length as reps_keys")
    for char in s:
        if char not in reps:
            raise ValueError(f"{char}: invalid option")
    for i in range(len(reps)):
        if reps[i] in s:
            return_list[i] = reps_keys[i]
    return return_list


numbers_to_special_characters_key = [")", "!", "@", "#", "$", "%", "^", "&", "*", "("]
