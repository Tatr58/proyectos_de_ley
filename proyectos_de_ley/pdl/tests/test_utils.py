import datetime

from django.test import TestCase

from pdl.utils import convert_string_to_time


class TestUtils(TestCase):
    def test_convert_string_to_time(self):
        string = "2014-10-10"
        expected = datetime.datetime(2014, 10, 10)
        result = convert_string_to_time(string)
        self.assertEqual(expected, result)

        string = "2014-10-10 10:20:10.23"
        expected = datetime.datetime(2014, 10, 10, 10, 20, 10, 230000)
        result = convert_string_to_time(string)
        self.assertEqual(expected, result)

        string = "2014-10-10 10:20:10"
        expected = datetime.datetime(2014, 10, 10, 10, 20, 10)
        result = convert_string_to_time(string)
        self.assertEqual(expected, result)

