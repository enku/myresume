"""Tests for the cli functions"""

# pylint: disable=missing-docstring

import os.path
import unittest
from unittest.mock import patch

import yaml
from unittest_fixtures import Fixtures, given

from myresume import cli

from . import lib

PARSER = cli.build_parser()
PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, "charlie.yaml"), encoding="utf8") as _fp:
    RESUME_STRUCT = yaml.load(_fp, Loader=yaml.SafeLoader)

del _fp


@given(lib.tempdir)
class TestArgumentParser(unittest.TestCase):
    def test(self, fixtures: Fixtures) -> None:
        tempdir = fixtures.tempdir
        yaml_path = os.path.join(tempdir, "myresume.yaml")

        with open(yaml_path, "w", encoding="utf8"):
            pass
        pdf = os.path.join(tempdir, "myresume.pdf")

        argv = ["--format=pdf", "--page-size=A4", "--public", yaml_path, pdf]

        args = PARSER.parse_args(argv)
        args.input.close()
        args.output.close()

        self.assertEqual(args.format, "pdf")
        self.assertEqual(args.pagesize, "A4")
        self.assertTrue(args.public)
        self.assertEqual(args.input.name, yaml_path)
        self.assertEqual(args.output.name, pdf)


@given(lib.tempdir)
class TestMain(unittest.TestCase):
    def test_writes_html(self, fixtures: Fixtures) -> None:
        tempdir = fixtures.tempdir
        resume_struct = RESUME_STRUCT.copy()
        del resume_struct["meta"]

        resume_yaml = yaml.dump(resume_struct)

        yaml_filename = os.path.join(tempdir, "resume.yaml")

        with open(yaml_filename, "wb") as yaml_file:
            yaml_file.write(resume_yaml.encode("utf-8"))

        resume_html = os.path.join(tempdir, "resume.html")
        argv = [yaml_filename, resume_html]
        status = cli.main(argv)

        self.assertTrue(os.path.exists(resume_html))

        with open(resume_html, "r", encoding="utf8") as html_file:
            fragment = html_file.read(15)

        self.assertEqual(fragment, "<!DOCTYPE html>")

        self.assertEqual(status, 0)

    def test_writes_pdf(self, fixtures: Fixtures) -> None:
        tempdir = fixtures.tempdir
        resume_struct = RESUME_STRUCT.copy()
        del resume_struct["meta"]

        resume_yaml = yaml.dump(resume_struct)

        yaml_filename = os.path.join(tempdir, "resume.yaml")

        with open(yaml_filename, "wb") as yaml_file:
            yaml_file.write(resume_yaml.encode("utf-8"))

        resume_pdf = os.path.join(tempdir, "resume.pdf")
        argv = ["--format", "pdf", yaml_filename, resume_pdf]

        with patch.object(cli.Resume, "to_pdf") as mock_to_pdf:
            mock_to_pdf.return_value = b"%PDF-1.4"
            status = cli.main(argv)

        self.assertTrue(os.path.exists(resume_pdf))

        with open(resume_pdf, "rb") as pdf_file:
            fragment = pdf_file.read(8)

        self.assertEqual(fragment, b"%PDF-1.4")

        self.assertEqual(status, 0)

    def test_writes_text(self, fixtures: Fixtures) -> None:
        tempdir = fixtures.tempdir
        resume_struct = RESUME_STRUCT.copy()
        del resume_struct["meta"]

        resume_yaml = yaml.dump(resume_struct)

        yaml_filename = os.path.join(tempdir, "resume.yaml")

        with open(yaml_filename, "wb") as yaml_file:
            yaml_file.write(resume_yaml.encode("utf-8"))

        resume_text = os.path.join(tempdir, "resume.txt")
        argv = ["--format", "text", yaml_filename, resume_text]

        status = cli.main(argv)

        self.assertTrue(os.path.exists(resume_text))

        with open(resume_text, "r", encoding="utf8") as text_file:
            text = text_file.read()

        self.assertTrue(text.startswith("Charlie Bucket\n\n1212"))

        self.assertEqual(status, 0)

    def test_with_meta(self, fixtures: Fixtures) -> None:
        tempdir = fixtures.tempdir
        resume_struct = RESUME_STRUCT.copy()

        resume_yaml = yaml.dump(resume_struct)

        yaml_filename = os.path.join(tempdir, "resume.yaml")

        with open(yaml_filename, "wb") as yaml_file:
            yaml_file.write(resume_yaml.encode("utf-8"))

        resume_html = os.path.join(tempdir, "resume.html")
        argv = [yaml_filename, resume_html]
        status = cli.main(argv)

        self.assertEqual(0, status)

        with open(resume_html, encoding="utf8") as fp:
            content = fp.read()

        self.assertIn("1971", content)
