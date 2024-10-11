import unittest

from ddt import data, ddt

from constants import CronFieldType
from parser import CronParser


@ddt
class TestParser(unittest.TestCase):

    @data(
        [
            "*/15 0 1,15 * 1-5 /usr/bin/find", # basic test case
            {
                CronFieldType.MINUTE: [0, 15, 30, 45],
                CronFieldType.HOURS: [0],
                CronFieldType.MONTH_DAY: [1, 15],
                CronFieldType.MONTH: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                CronFieldType.WEEK_DAY: [1, 2, 3, 4, 5],
                'command': '/usr/bin/find',
            }
        ],
        [
            "* * * * * /usr/bin/find", # All stars
            {
                CronFieldType.MINUTE: list(range(0, 60)),
                CronFieldType.HOURS: list(range(0, 24)),
                CronFieldType.MONTH_DAY: list(range(1, 32)),
                CronFieldType.MONTH: list(range(1, 13)),
                CronFieldType.WEEK_DAY: list(range(1, 8)),
                'command': '/usr/bin/find',
            }
        ],
        [
            "1-30 * 1-15 * 1,2,5 /usr/bin/find", # Multiple comma separated values
            {
                CronFieldType.MINUTE: list(range(1, 31)),
                CronFieldType.HOURS: list(range(0, 24)),
                CronFieldType.MONTH_DAY: list(range(1, 16)),
                CronFieldType.MONTH: list(range(1, 13)),
                CronFieldType.WEEK_DAY: [1, 2, 5],
                'command': '/usr/bin/find',
            }
        ],
        [
            "2/15 0 1,15 * 1-5 /usr/bin/find",  # start of interval defined
            {
                CronFieldType.MINUTE: [2, 17, 32, 47],
                CronFieldType.HOURS: [0],
                CronFieldType.MONTH_DAY: [1, 15],
                CronFieldType.MONTH: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                CronFieldType.WEEK_DAY: [1, 2, 3, 4, 5],
                'command': '/usr/bin/find',
            }
        ],
    )
    def test_success(self, params):
        cron_string = params[0]
        expected_output = params[1]
        cron_parser = CronParser(cron_string)
        cron_parser.process()
        self.assertDictEqual(cron_parser.get_result_dict(), expected_output)

    @data(
        "abc def",
        "string with six words to verify",
        "*/15 0 1,15 * /usr/bin/find", # missing day of week
        "1/15 * 1,15 ^ 1-5 /usr/bin/find",  # Invalid symbol used
        "5/0 * 1,15 * 1-5 /usr/bin/find",  # Interval is zero
        "40-70 * 1-15 * 1-5 /usr/bin/find",  # Range out of bounds for minutes field
        "1-30 * 25,30 1,2 * /usr/bin/find",  # 30th day not available for February
        ""
    )
    def test_failure(self, value):
        cron_string = value
        with self.assertRaises(ValueError):
            cron_parser = CronParser(cron_string)
            cron_parser.process()