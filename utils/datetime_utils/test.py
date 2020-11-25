import unittest

from utils import datetime_utils


class TestDateTimeUtils(unittest.TestCase):

    def test_ms_to_age(self):
        self.assertEqual(datetime_utils.ms_to_age(626294000), (7, 5, 58, 14))

    def test_ms_to_age_string(self):
        self.assertEqual(datetime_utils.ms_to_age_string(626294000), '7 days, 5 hours, 58 minutes, 14 seconds')
        self.assertEqual(datetime_utils.ms_to_age_string(608294000), '7 days, 58 minutes, 14 seconds')
        self.assertEqual(datetime_utils.ms_to_age_string(608280000), '7 days, 58 minutes')
