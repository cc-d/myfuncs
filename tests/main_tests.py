import unittest
from unittest.mock import patch
from subprocess import CompletedProcess
import sys
from pathlib import Path
import os

from myfuncs import runcmd  # noqa

class TestRunCmd(unittest.TestCase):
    def test_runcmd_with_output(self):
        # Mock the subprocess.run() function to return a CompletedProcess object
        mock_completed_process = CompletedProcess(
            args=['echo', 'Hello, World!'],
            returncode=0,
            stdout='Hello, World!\n',
            stderr=''
        )
        with patch('subprocess.run', return_value=mock_completed_process):
            result = runcmd('echo Hello, World!')

        self.assertEqual(result, ['Hello, World!'])

    def test_runcmd_without_output(self):
        # Mock the subprocess.run() function to return None
        with patch('subprocess.run'):
            result = runcmd('echo Hello, World!', output=False)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
