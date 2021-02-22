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


def parse_cli_args(args=None):
    parser = argparse.ArgumentParser(description=unique_chars.__doc__)
    parser.add_argument('-s', '--strings', nargs='+')
    parser.add_argument('-f', '--file', nargs='+')
    namespace = parser.parse_args(args)
    return namespace, parser


def main(cli_args=None):
    cli_ns, parser = parse_cli_args(cli_args)

    # 'file' option has priority over the entered strings
    if cli_ns.file:
        with open(*cli_ns.file, 'r') as f:
            input_strings = f.readlines()
    else:
        input_strings = cli_ns.strings

    # if nothing is passed, print help and exit
    if not input_strings:
        parser.print_help()
        exit()

    # print the output of the program
    for string in input_strings:
        print(unique_chars(string))


if __name__ == '__main__':
    main()
