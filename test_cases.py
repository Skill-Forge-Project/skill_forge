import unittest
import io
import contextlib
import re


def is_palindrome(s):
    return s


class TestIsPalindrome(unittest.TestCase):
    def test_palindrome(self):
        self.assertEqual(is_palindrome("radar"), 'radar')
    def test_palindrome_2(self):
        self.assertEqual(is_palindrome("level"), 'level')

if __name__ == '__main__':
    # unittest.main()
    import __main__
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    pattern = r'(?P<1>^Ran.*s$)\n\n((?P<2>^FA.*)|(?P<3>OK))'
    
    with io.StringIO() as buf:
        # run the tests
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf).run(suite)
        # process (in this case: print) the results
        result = str(buf.getvalue())
        print(result)
        pattern = re.compile(r'(?P<1>^Ran.*s$)\n\n((?P<2>^FA.*)|(?P<3>OK))')

        # find all matches to groups
        for match in pattern.finditer(result):
            # extract words
            print(match.group("1"))
            # extract numbers
            print(match.group(2))
