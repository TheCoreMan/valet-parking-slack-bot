# Testing the SQLAlchemy models.
import pytest
import sqlalchemy
from valet_parking_slack_bot.model.db_factory import (
        get_session_for_case,
        DbCase,
)

@pytest.mark.parametrize(
    "db_case", 
    [
        DbCase.inmem_testing,
    ] # TODO - add more DbCases once we implement them.
)
def test_db_session(db_case: DbCase):
    expected = "asdfzcxv"
    session = get_session_for_case(db_case)
    result = session.execute(sqlalchemy.text(f"select '{expected}'"))
    assert expected == result.all()[0][0]

