"""My resume tests library"""

# pylint: disable=missing-docstring
import tempfile
from unittest import mock

from unittest_fixtures import FixtureContext, Fixtures, fixture


@fixture()
def tempdir(_: Fixtures) -> FixtureContext[str]:
    with tempfile.TemporaryDirectory() as dirname:
        yield dirname


@fixture()
def to_pdf(_: Fixtures) -> FixtureContext[mock.Mock]:
    with mock.patch("myresume.cli.Resume.to_pdf") as mock_to_pdf:
        yield mock_to_pdf
