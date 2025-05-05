"""Tests for the Jinja2 filters"""
# pylint: disable=missing-docstring

import unittest

from myresume import filters


class TestRegexReplace(unittest.TestCase):
    def test(self):
        text = "To be or not to be? That is the question."
        output = filters.regex_replace(text, "be", "code", 1)

        expected = "To code or not to be? That is the question."
        self.assertEqual(output, expected)


class TestPrettyUrl(unittest.TestCase):
    def test_url_with_non_standard_port(self):
        url = "http://bighost.invalid:8080/foo/"

        result = filters.pretty_url(url)

        self.assertEqual(result, "bighost.invalid:8080/foo")

    def test_url_with_standard_port(self):
        url = "https://bighost.invalid:443/foo/"

        result = filters.pretty_url(url)

        self.assertEqual(result, "bighost.invalid/foo")

    def test_url_without_port(self):
        url = "http://bighost.invalid/foo/"

        result = filters.pretty_url(url)

        self.assertEqual(result, "bighost.invalid/foo")

    def test_url_with_querystring(self):
        url = "http://bighost.invalid/foo?q=candidates"

        result = filters.pretty_url(url)

        self.assertEqual(result, "bighost.invalid/foo")

    def test_test_tel_url(self):
        url = "tel:212-555-1212"

        result = filters.pretty_url(url)

        self.assertEqual(result, "212•555•1212")
