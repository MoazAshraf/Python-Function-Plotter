from plotter.util import split_str


def test_split_str_no_whitespace_comma():
    string = "a,b,1,2,abc,123,*&#!,"
    expected = ["a",",","b",",","1",",","2",",","abc",",","123",",","*&#!",","]
    assert split_str(string, sep=[',']) == expected

def test_split_str_whitespace_comma():
    string = "  a, b, 1, 2, \t\nabc, 123,   \t*&#!,\n\n"
    expected = ["a",",","b",",","1",",","2",",","abc",",","123",",","*&#!",","]
    assert split_str(string, sep=[',']) == expected

def test_split_str_intmath():
    string = "-x * 4.0^2.33 - 4912 / 6.559 + 9"
    expected = ["-", "x", "*", "4.0", "^", "2.33", "-", "4912", "/", "6.559",
                "+", "9"]
    assert split_str(string, sep=['+', '-', '*', '/', '^']) == expected

# TODO: test empty strings, strings with no separators, strings with white space
# between operands