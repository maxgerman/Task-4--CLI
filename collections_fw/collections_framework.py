"""
Count the number of the unique characters in the strings of passed arguments or a file

    Functions:

        unique_chars(input_string: str) -> int
        parse_cli_args(args: list = None) -> (argparse.Namespace, argparse.ArgumentParser)
"""

from collections import Counter
from functools import lru_cache
import argparse


@lru_cache
def unique_chars(input_string: str) -> int:
    """Return the number of unique characters in the string."""
    if not isinstance(input_string, str):
        raise TypeError(f'String expected, got {type(input_string)}')
    c = Counter(input_string)
    # old version, creates list in the memory; amended to the generator and sum func.
    # unique_sum = len([key for key, val in c.items() if val == 1])
    unique_sum = sum(num for num in c.values() if num == 1)
    return unique_sum


def parse_cli_args(args: str = None) -> (argparse.Namespace, argparse.ArgumentParser):
    """
    Create CLI parser and parse arguments. Return the namespace object with parsed strings as properties and the parser.

    Keyword argument:
    args -- arbitrary list can be passed as arguments. If none, actual CLI args are used.
    """
    parser = argparse.ArgumentParser(description=unique_chars.__doc__, prog='Collections framework')
    parser.add_argument('-s', '--strings', nargs='+', help='Strings to be parsed')
    parser.add_argument('-f', '--file', nargs='+', help='File to be parsed, each line will be counted separately')
    namespace = parser.parse_args(args)
    return namespace, parser


def main(cli_args: list = None):
    """Start the program, process the CLI arguments. Kwarg 'cli_args' can be used for custom strings instead of CLI."""
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
