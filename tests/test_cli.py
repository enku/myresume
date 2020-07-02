"""Tests for the cli functions"""
import os.path
import sys
import tempfile
import unittest

import yaml

from myresume import cli

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, "charlie.yaml")) as fp:
    RESUME_STRUCT = yaml.load(fp, Loader=yaml.SafeLoader)


class TestParseArgs(unittest.TestCase):
    def test(self):
        with tempfile.TemporaryDirectory() as tempdir:
            yaml = os.path.join(tempdir, "myresume.yaml")
            yaml_file = open(yaml, "w")
            yaml_file.close()
            pdf = os.path.join(tempdir, "myresume.pdf")

            argv = ["--format=pdf", "--page-size=A4", "--public", yaml, pdf]

            args = cli.parse_args(argv)
            args.input.close()
            args.output.close()

        self.assertEqual(args.format, "pdf")
        self.assertEqual(args.pagesize, "A4")
        self.assertTrue(args.public)
        self.assertEqual(args.input.name, yaml)
        self.assertEqual(args.output.name, pdf)


class TestMain(unittest.TestCase):
    def test_writes_html(self):
        resume_struct = RESUME_STRUCT.copy()
        del resume_struct["meta"]

        resume_yaml = yaml.dump(resume_struct)

        with tempfile.TemporaryDirectory() as tempdir:
            yaml_filename = os.path.join(tempdir, "resume.yaml")

            with open(yaml_filename, "wb") as yaml_file:
                    yaml_file.write(resume_yaml.encode("utf-8"))

            resume_html = os.path.join(tempdir, "resume.html")
            argv = [yaml_filename, resume_html]
            status = cli.main(argv)

            self.assertTrue(os.path.exists(resume_html))

            with open(resume_html, "r") as html_file:
                fragment = html_file.read(15)

            self.assertEqual(fragment, "<!DOCTYPE html>")

        self.assertEqual(status, 0)

    def test_writes_pdf(self):
        resume_struct = RESUME_STRUCT.copy()
        del resume_struct["meta"]

        resume_yaml = yaml.dump(resume_struct)

        with tempfile.TemporaryDirectory() as tempdir:
            yaml_filename = os.path.join(tempdir, "resume.yaml")

            with open(yaml_filename, "wb") as yaml_file:
                    yaml_file.write(resume_yaml.encode("utf-8"))

            resume_pdf = os.path.join(tempdir, "resume.pdf")
            argv = ["--format", "pdf", yaml_filename, resume_pdf]
            status = cli.main(argv)

            self.assertTrue(os.path.exists(resume_pdf))

            with open(resume_pdf, "rb") as pdf_file:
                fragment = pdf_file.read(8)

            self.assertEqual(fragment, b"%PDF-1.4")

        self.assertEqual(status, 0)
