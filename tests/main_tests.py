import unittest
from subprocess import CompletedProcess
import sys
from pathlib import Path
import os
from unittest.mock import patch, MagicMock, call
from os.path import dirname, abspath
from typing import *

MFROOT = str(dirname(dirname(abspath(__file__))))
if MFROOT not in sys.path:
    sys.path.insert(0, MFROOT)

from myfuncs import (
    runcmd,
    objinfo,
    nlprint,
    is_jwt_str,
    ranstr,
    get_terminal_width,
    print_middle,
    print_columns,
    ALPHANUMERIC_CHARS,
)


class TestRunCmd(unittest.TestCase):
    def test_runcmd_with_output(self):
        # Mock the subprocess.run() function to return a CompletedProcess object
        mock_completed_process = CompletedProcess(
            args=['echo', 'Hello, World!'],
            returncode=0,
            stdout='Hello, World!\n',
            stderr='',
        )
        with patch('subprocess.run', return_value=mock_completed_process):
            result = runcmd('echo Hello, World!')

        self.assertEqual(result, ['Hello, World!'])

    def test_runcmd_without_output(self):
        # Mock the subprocess.run() function to return None
        with patch('subprocess.run'):
            result = runcmd('echo Hello, World!', output=False)

        self.assertIsNone(result)


class TestPrintMiddle(unittest.TestCase):
    @patch("myfuncs.get_terminal_width", return_value=50)
    def test_print_middle_no_print(self, *args):
        tstr = '012345678901'
        clen = (50 - len(f' {tstr} ')) // 2
        with patch('builtins.print') as mock_print:
            result = print_middle(tstr, noprint=True)
        self.assertEqual(result, f'{clen * "="} {tstr} {clen * "="}')
        mock_print.assert_not_called()


class TestGetTerminalWidth(unittest.TestCase):
    def test_default_terminal_width(self):
        # When there's an OSError exception
        with patch('os.get_terminal_size', side_effect=OSError):
            result = get_terminal_width()
        self.assertEqual(result, 80)

    def test_actual_terminal_width(self):
        with patch(
            'os.get_terminal_size', return_value=os.terminal_size((100, 24))
        ):
            result = get_terminal_width()
        self.assertEqual(result, 100)


class TestPrintColumns(unittest.TestCase):
    @patch("myfuncs.get_terminal_width", return_value=80)
    @patch("builtins.print")
    def test_print_columns_basic(self, mock_print, mock_get_terminal_width):
        items = [
            'a',
            'aa',
            'aaa',
            'aaaa',
            'aaaaa',
            'aaaaaa',
            'aaaaaaa',
            'aaaaaaaa',
            'aaaaaaaaa',
        ]
        print_columns(items)

        mock_print.assert_called_with(
            'aaaaaaaa   aaaaaaaaa'
        )  # This verifies the last call to print function

    @patch("myfuncs.get_terminal_width", return_value=40)
    @patch("builtins.print")
    def test_print_columns_small_terminal(
        self, mock_print, mock_get_terminal_width
    ):
        items = [
            'a',
            'aa',
            'aaa',
            'aaaa',
            'aaaaa',
            'aaaaaa',
            'aaaaaaa',
            'aaaaaaaa',
            'aaaaaaaaa',
        ]
        print_columns(items)

        mock_print.assert_called_with(
            'aaaaaaa    aaaaaaaa   aaaaaaaaa'
        )  # This verifies the last call to print function

    @patch("myfuncs.get_terminal_width", return_value=80)
    @patch("builtins.print")
    def test_print_columns_sorted(self, mock_print, mock_get_terminal_width):
        items = ['b', 'a', 'c']
        print_columns(items)

        mock_print.assert_called_with(
            'a  b  c'
        )  # This verifies the last call to print function


class TestRanStr(unittest.TestCase):
    def test_string_length(self):
        result = ranstr(5, 10)
        self.assertTrue(5 <= len(result) <= 10)

    def test_string_characters(self):
        chars = 'abcd'
        result = ranstr(5, 10, chars=chars)
        for char in result:
            self.assertIn(char, chars)

    def test_return_generator(self):
        result = ranstr(5, 10, as_generator=True)
        self.assertIsInstance(result, Generator)
        generated_string = ''.join(result)
        self.assertTrue(5 <= len(generated_string) <= 10)

    def test_return_string(self):
        result = ranstr(5, 10)
        self.assertIsInstance(result, str)
        self.assertTrue(5 <= len(result) <= 10)


if __name__ == '__main__':
    unittest.main()
