from api.tests.asserts import are_equal
import pytest
from yards_py.domain.entities.team import Team
from yards_py.domain.entities.state import Locks

test_cases = [
    ({}, False),  # No teams locked
    ({"BC": True}, True),
    ({"CGY": True}, True),
    ({"EDM": True}, True),
    ({"SSK": True}, True),
    ({"WPG": True}, True),
    ({"HAM": True}, True),
    ({"TOR": True}, True),
    ({"OTT": True}, True),
    ({"MTL": True}, True),
]


@pytest.mark.parametrize("locked_team, expected", test_cases)
def test_any_locks_works_with_all_teams(locked_team: Team, expected: bool):
    locks = Locks(**locked_team)

    actual = locks.any_locks()
    are_equal(expected, actual)
