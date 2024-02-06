import datetime
import locale
import os.path
import subprocess
import unittest
from unittest.mock import patch

import yaml

import myresume

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, "charlie.yaml")) as fp:
    RESUME_STRUCT = yaml.load(fp, Loader=yaml.SafeLoader)

locale.setlocale(locale.LC_ALL, "en_US")


class TestResume(unittest.TestCase):
    def test_init_saves_copy_of_struct(self):
        resume = myresume.Resume(RESUME_STRUCT)

        self.assertIsNot(RESUME_STRUCT, resume.context)

    def test_to_html_renders_html(self):
        resume = myresume.Resume(RESUME_STRUCT)
        result = resume.to_html()

        self.assertTrue(
            result.startswith("<!DOCTYPE html>"),
            "Output looks weird: %s..." % result[:20],
        )

    def test_to_pdf_renders_pdf(self):
        resume = myresume.Resume(RESUME_STRUCT)

        with patch.object(myresume.subprocess, "Popen") as mock_popen:
            mock_popen.return_value.stdout.return_value = b"%PDF-1.4\n"
            result = resume.to_pdf()

        self.assertTrue(
            result.startswith(b"%PDF-1.4\n"),
            "Output looks weird: %s..." % result[:9],
        )
        mock_popen.assert_called_once_with(
            [
                "wkhtmltopdf",
                "--quiet",
                "--page-size",
                "Letter",
                "--print-media-type",
                "-",
                "-",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        html = resume.to_html()
        mock_popen.return_value.stdin.write.assert_called_once_with(
            html.encode("utf-8")
        )

    def test_date_filter(self):
        resume = myresume.Resume(RESUME_STRUCT)
        html = resume.to_html()

        self.assertNotIn("Chocolatier", html)

    def test_privacy_filter(self):
        struct = RESUME_STRUCT.copy()
        struct["meta"]["public"] = True
        context = myresume.Resume(struct).context

        self.assertEqual(context["contactInfo"]["address"], "")
        self.assertEqual(
            context["links"],
            [{"name": "Social", "url": "https://spitter.invalid/charlie/"}],
        )

    def test_str(self):
        resume = myresume.Resume(RESUME_STRUCT)

        self.assertEqual(str(resume), resume.to_html())

    def test_context_should_contain_myresume_version(self):
        resume = myresume.Resume(RESUME_STRUCT)

        expected = myresume.version()
        self.assertEqual(resume.context["meta"]["myresume"]["version"], expected)


class TestFilterDates(unittest.TestCase):
    def test(self):
        entries = RESUME_STRUCT["sections"][0]["entries"]

        recent, old = myresume.filter_dates(entries, 2007)

        self.assertEqual(len(old), 1)
        self.assertEqual(len(recent), 1)

        self.assertEqual(old[0]["role"], "Chocolatier")
        self.assertEqual(recent[0]["role"], "Programmer")


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
