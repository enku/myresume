# pylint: disable=missing-docstring
import datetime
import locale
import unittest
from copy import deepcopy

import myresume

from . import lib

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class TestResume(unittest.TestCase):
    def test_init_saves_copy_of_struct(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)

        self.assertIsNot(lib.RESUME_STRUCT, resume.context)

    def test_to_html_renders_html(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)
        result = resume.to_html()

        self.assertTrue(
            result.startswith("<!DOCTYPE html>"),
            f"Output looks weird: {result[:20]}...",
        )

    def test_to_pdf_renders_pdf(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)
        result = resume.to_pdf()

        self.assertTrue(
            result.startswith(b"%PDF-1.7\n"), f"Output looks weird: {result[:9]}..."
        )

    def test_to_text_renders_test(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)
        result = resume.to_text()

        self.assertTrue(
            result.startswith("Charlie"), f"Output looks weird: {result[:9]}..."
        )

    def test_date_filter(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)
        html = resume.to_html()

        self.assertNotIn("Chocolatier", html)

    def test_privacy_filter(self):
        struct = lib.RESUME_STRUCT.copy()
        struct["meta"]["public"] = True
        context = myresume.Resume(struct).context

        self.assertEqual(context["contactInfo"]["address"], "")
        self.assertEqual(
            context["links"],
            [{"name": "Social", "url": "https://spitter.invalid/charlie/"}],
        )

    def test_str(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)

        self.assertEqual(str(resume), resume.to_html())

    def test_context_should_contain_myresume_version(self):
        resume = myresume.Resume(lib.RESUME_STRUCT)

        expected = myresume.version()
        self.assertEqual(resume.context["meta"]["myresume"]["version"], expected)


class TestFilterDates(unittest.TestCase):
    def test(self):
        entries = lib.RESUME_STRUCT["sections"][0]["entries"]

        recent, old = myresume.filter_dates(entries, 2007)

        self.assertEqual(len(old), 1)
        self.assertEqual(len(recent), 1)

        self.assertEqual(old[0]["role"], "Chocolatier")
        self.assertEqual(recent[0]["role"], "Programmer")

    def test_when_to_is_present_goes_to_current(self):
        entries = deepcopy(lib.RESUME_STRUCT["sections"][0]["entries"])
        del entries[-1]["to"]

        recent = myresume.filter_dates(entries, 2007)[0]

        self.assertIn(entries[-1], recent)


class TestToDate(unittest.TestCase):
    def test_with_only_year(self):
        # If reading from YAML, if the value is just a year and isn't quoted then it's
        # actually an int
        date_str = 1933

        dt_object = myresume.to_date(date_str)

        self.assertEqual(dt_object, datetime.date(1933, 1, 1))

    def test_with_month_and_year(self):
        date_str = "June 1933"

        dt_object = myresume.to_date(date_str)

        self.assertEqual(dt_object, datetime.date(1933, 6, 1))
