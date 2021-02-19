from collections import Counter
from functools import lru_cache
import argparse


@lru_cache
def unique_chars(input_string: str) -> int:
    """returns the number of unique characters in the string; has cache"""
    if not isinstance(input_string, str):
        raise TypeError(f'String expected, got {type(input_string)}')
    c = Counter(input_string)
    ul = len([key for key, val in c.items() if val == 1])
    return ul


def main():
    parser = argparse.ArgumentParser(description=unique_chars.__doc__)
    parser.add_argument('-s', '--strings', nargs='+')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'))
    p = parser.parse_args()


    if not p.file and not p.strings:
        parser.print_help()
        exit()

    # 'file' option has priority over the entered strings
    input_strings = p.file.read().split() if p.file else p.strings

    for string in input_strings:
        print(unique_chars(string))


if __name__ == '__main__':
    main()
