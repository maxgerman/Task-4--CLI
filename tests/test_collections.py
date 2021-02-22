import pytest
from unittest import mock
from collections_fw import unique_chars
from collections_fw import collections_framework

typical_param = [
    ('abbbccdf', 3),
    ('aaaaaa', 0),
    ('abcdefg', 7),
    ('abcdeee', 4),
    ('abc', 3),
    ('abc', 3),  # to increase the hits counter

]

CLI_typical_str_params = [
    (['--string', 'abbbccdf'], 3),
    (['--string', 'aaaaaa'], 0),
    # passing multiple strings
    (['--string', 'abcc', 'defg', '123'], '2\n4\n3'),
    # using shortened key '-s',
    (['-s', 'abcdeee'], 4),
    (['-s', 'abc'], 3),
]

CLI_parser_params = [
    (['-s', 'abc'], 'strings', 'abc'),
    (['--strings', 'abcd'], 'strings', 'abcd'),
    (['-f', 'example.txt'], 'file', 'example.txt'),
    (['--file', 'example2.txt'], 'file', 'example2.txt'),
]


def test_unique_chars_typical():
    for inp_val, out_val in typical_param:
        assert unique_chars(inp_val) == out_val


def test_unique_chars_atypical():
    with pytest.raises(TypeError):
        unique_chars(123)


def test_lru_cache_hits():
    '''check if cache is hitting'''
    assert unique_chars.cache_info()[0] > 0


@pytest.mark.parametrize('test_input, expected', CLI_typical_str_params)
def test_strings_from_CLI(test_input, expected, monkeypatch, capfd):
    """tests that input is read form the CLI and the correct prints are made in response"""
    test_argv = ['progname', *test_input]
    monkeypatch.setattr('sys.argv', test_argv)
    collections_framework.main()
    out, err = capfd.readouterr()
    assert out.rstrip() == str(expected)


@pytest.mark.parametrize('test_input, property, expected', CLI_parser_params)
def test_parser(test_input, property, expected):
    """tests that parser receives and stores CLI parameters in the appropriate properties"""
    test_ns, parser = collections_framework.parse_cli_args(test_input)
    assert getattr(test_ns, property)[0] == expected


def test_parser_file(capfd):
    """reading from a mock file, asserting correct prints"""
    mock_file_contents = 'this is an example text file'
    with mock.patch('collections_fw.collections_framework.open', mock.mock_open(read_data=mock_file_contents)) as m:
        collections_framework.main(['-f', 'example.txt'])
    # reading the prints of the main() function
    out, err = capfd.readouterr()
    assert out.rstrip() == str(unique_chars(mock_file_contents))
