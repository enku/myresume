"""My resume tests library"""

# pylint: disable=missing-docstring
import os
import tempfile
from unittest import mock

import yaml
from unittest_fixtures import FixtureContext, Fixtures, fixture

PATH = os.path.dirname(__file__)
with open(os.path.join(PATH, "charlie.yaml"), encoding="utf8") as _fp:
    RESUME_STRUCT = yaml.load(_fp, Loader=yaml.SafeLoader)

del _fp


@fixture()
def tempdir(_: Fixtures) -> FixtureContext[str]:
    with tempfile.TemporaryDirectory() as dirname:
        yield dirname


@fixture()
def to_pdf(_: Fixtures) -> FixtureContext[mock.Mock]:
    with mock.patch("myresume.cli.Resume.to_pdf") as mock_to_pdf:
        yield mock_to_pdf
