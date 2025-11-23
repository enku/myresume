"""My resume tests library"""

# pylint: disable=missing-docstring
import tempfile

from unittest_fixtures import FixtureContext, Fixtures, fixture


@fixture()
def tempdir(_: Fixtures) -> FixtureContext[str]:
    with tempfile.TemporaryDirectory() as dirname:
        yield dirname
