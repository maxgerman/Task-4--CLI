import pytest
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


# todo: test priority; multiline text files

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
    test_argv = ['progname', *test_input]
    monkeypatch.setattr('sys.argv', test_argv)
    collections_framework.main()
    out, err = capfd.readouterr()
    assert out.rstrip() == str(expected)


#  file mocking - not working yet
#
# def test_file_from_CLI(monkeypatch, capfd):
#     class Mock_TextIOWrapper:
#         """mock _io.TextIOWrapper class"""
#
#         @staticmethod
#         def read():
#             return "mock file text"
#
#     def mock_read(*args, **kwargs):
#         """ mocked return of the text file reading"""
#         return Mock_TextIOWrapper()
#
#     test_argv = ['progname', '--file', 'test.txt']
#     monkeypatch.setattr('sys.argv', test_argv)
#     monkeypatch.setattr('collections_framework.TextIOWrapper', 'read', mock_read)
#     collections_framework.main()
