#!/usr/bin/env python3
import logging
import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))  # Add the parent directory of tests to the system path

from myfuncs.funcs import logf, get_asctime, valid_uuid

logging.basicConfig(level=logging.DEBUG)

class TestMyFuncs(unittest.TestCase):
    def test_get_asctime(self):
        asctime = get_asctime()
        self.assertIsNotNone(asctime)
        self.assertIsInstance(asctime, str)

    def test_valid_uuid(self):
        uuid_valid = "123e4567-e89b-12d3-a456-426614174000"
        uuid_invalid = "123e4567-e89b-12d3-a456-42661417400"

        self.assertTrue(valid_uuid(uuid_valid))
        self.assertFalse(valid_uuid(uuid_invalid))

    def test_logf_decorator(self):
        logger_mock = MagicMock()

        @logf(level=logging.DEBUG, log_args=True, log_return=True, measure_time=True)
        def example_func(a, b):
            return a + b

        with unittest.mock.patch('myfuncs.funcs.logger', logger_mock):
            result = example_func(1, 2)

        self.assertEqual(result, 3)
        self.assertEqual(logger_mock.log.call_count, 2)
        logger_mock.log.assert_any_call(logging.DEBUG, "example_func() | (1, 2) {}")
        log_message = logger_mock.log.call_args_list[1][0][1]
        self.assertTrue(log_message.startswith("example_func()"))
        self.assertTrue(log_message.endswith(" | 3"))


if __name__ == "__main__":
    unittest.main()
