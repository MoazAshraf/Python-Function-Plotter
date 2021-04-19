from plotter.util import split_str


class TestSplitStr(object):
    def test_empty(self):
        string = ""
        expected = []
        assert split_str(string, sep=[',']) == expected

    def test_no_whitespace_comma(self):
        string = "a,b,1,2,abc,123,*&#!,"
        expected = ['a', ',', 'b', ',', '1', ',', '2', ',', 'abc', ',',
                    '123', ',', '*&#!', ',']
        assert split_str(string, sep=[',']) == expected

    def test_whitespace_comma(self):
        string = "  a, b, 1, 2, \t\nabc, 123,   \t*&#!,\n\n"
        expected = ['  a', ',', ' b', ',', ' 1', ',', ' 2', ',', ' \t\nabc',
                    ',', ' 123', ',', '   \t*&#!', ',', '\n\n']
        assert split_str(string, sep=[',']) == expected

    def test_intmath(self):
        string = "-x * 4.0^2.33 - 4912 / 6.559 + 9"
        expected = ['-', 'x ', '*', ' 4.0', '^', '2.33 ', '-', ' 4912 ', '/',
                    ' 6.559 ', '+' ,' 9']
        assert split_str(string, sep=['+', '-', '*', '/', '^']) == expected

    def test_nosep(self):
        string = "abcdefg"
        expected = ['abcdefg']
        assert split_str(string, sep=[',']) == expected

    def test_nosep_whitespace(self):
        string = "abc def"
        expected = ['abc def']
        assert split_str(string, sep=[',']) == expected
    
    def test_nosep_whitespace_float(self):
        string = "40 . 22"
        expected = ['40 . 22']
        assert split_str(string, sep=[',']) == expected