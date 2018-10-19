class Token:
    STRING_BEGIN = STRING_END = '"'
    LIST_BEGIN = '['
    LIST_END = ']'
    LIST_DELIMITER = DICT_DELIMITER = ','
    DICT_SYMBOL = ':'
    DICT_BEGIN = '{'
    DICT_END = '}'
    WHITESPACE = ' '
    NEWLINE = '\n'


class ParserException(Exception):
    pass


def isdigit(s):
    return s in "01234567890"


def parse_string(string):
    json_string = ''
    if string[0] == Token.STRING_BEGIN:
        string = string[1:]
    else:
        return None, string
    for c in string:
        if c == Token.STRING_END:
            return json_string, string[len(json_string) + 1:]
        else:
            json_string += c

    raise Exception('Expected end-of-string quote')
    pass


def parse_number(string):
    number = []
    for s in string:
        if s in "01234567890":
            number.append(s)
        else:
            break
    return int("".join(number)), string[len(number):]


def parse_json_array(string):
    json_array = []
    string = string[1:]
    while len(string):
        if string[0] == Token.LIST_DELIMITER:
            string = string[1:]
        elif string[0] == Token.LIST_END:
            string = string[1:]
            break
        key, string = parse(string)
        json_array.append(key)
    return json_array, string


def parse_json_object(string):
    json_object = {}
    string = string[1:]
    while len(string):
        if string[0] == Token.DICT_DELIMITER:
            string = string[1:]
        elif string[0] == Token.DICT_END:
            string = string[1:]
            break
        key, string = parse(string)
        string = string[1:]
        val, string = parse(string)
        json_object[key] = val
    return json_object, string


def parse(string):
    s = string[0]
    if s == Token.STRING_BEGIN:
        return parse_string(string)
    elif s == Token.LIST_BEGIN:
        return parse_json_array(string)
    elif s == Token.DICT_BEGIN:
        return parse_json_object(string)
    elif isdigit(s):
        return parse_number(string)
    else:
        raise ParserException("Unknown Token: %s" % s)


assert parse('123') == (123, '')
assert parse('123abc') == (123, 'abc')
assert parse('"123"abc') == ('123', 'abc')
assert parse('"abc"[123]') == ('abc', '[123]')
assert parse('[1,2,3]') == ([1, 2, 3], '')
assert parse('[1,2,3][abc]') == ([1, 2, 3], '[abc]')
assert parse('[[[]]]') == ([[[]]], '')
assert parse('[[],[[]]]') == ([[], [[]]], '')
assert parse('["a",123,["x","y"]]') == (["a", 123, ["x", "y"]], '')
assert parse('{"a":1}') == ({"a": 1}, '')
assert parse('{"a":1,"b":2}') == ({"a": 1, "b": 2}, '')
assert parse('{}') == ({}, '')
assert parse('{}abc') == ({}, 'abc')
assert parse('{"a":[[[]]]}') == ({"a": [[[]]]}, '')
assert parse('{"a":1,"b":[1,2,3],"c":{"d":1}}') == ({"a": 1, "b": [1, 2, 3], "c": {"d": 1}}, '')