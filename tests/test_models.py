# Testing the SQLAlchemy models.
import logging
import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, date
from valet_parking_slack_bot.model.db_factory import (
        get_session_for_case,
        DbCase,
)
from valet_parking_slack_bot.model.models import (
    create_all_tables,
    Garage,
    Spot,
    User,
    Reservation,
    PricingTier,
    Workspace,
)

logger = logging.getLogger(__name__)

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


def test_running_create_all_tables_twice_is_safe():
    session: Session = get_session_for_case(DbCase.inmem_testing)
    create_all_tables(session)
    create_all_tables(session)

def test_workspace_model_sanity():
    session: Session = get_session_for_case(DbCase.inmem_testing)
    create_all_tables(session)

    workspace_1 = Workspace(
        name="test_workspace",
        pricing_tier=PricingTier.free,
        onboard_time=datetime.now(),
    )
    
    assert workspace_1.id is None, "not added to session"
    session.add(workspace_1)
    session.flush()
    assert workspace_1.id is not None, "should have been added to session"
    result = session.execute(select(Workspace))
    entities = result.scalars().all()
    assert len(entities) == 1
    assert entities[0].name == "test_workspace"


DEMO_WORKSPACE_NAME = "NiceFam"
DEMO_WORKSPACE_SLACK_ID = "T02CPGASL8Y"
DEMO_MEMBER_ID = "U02C63W148L"
DEMO_RESERVATION_DATE = date(1994, 10, 19)

@pytest.fixture(scope="class")
def session_with_demo_models(request):
    session: Session = get_session_for_case(DbCase.inmem_testing)
    create_all_tables(session)

    # first, set up a workspace
    w1 = Workspace(
        slack_id=DEMO_WORKSPACE_SLACK_ID,
        name=DEMO_WORKSPACE_NAME,
        pricing_tier=PricingTier.paid, 
        onboard_time=datetime.now()
    )
    g1 = Garage(
        name="Main garage",
        full_instructions="it's full, you're fucked.",
        arrival_instructions="just get here",
    )
    spots = [Spot(name="1"), Spot(name="2"), Spot(name="3")]
    for s in spots:
        g1.spots.append(s)
    w1.garages.append(g1)
    
    session.add(w1)

    # now add some reservations
    r1 = Reservation(
        date=DEMO_RESERVATION_DATE, 
        active=True, 
        member_id=DEMO_MEMBER_ID,
        member_name="Shay Nehmad",
        spot=spots[0],
    )
    r2 = Reservation(
        date=datetime.now(),
        active=False,
        member_id=DEMO_MEMBER_ID,
        member_name="Shay Nehmad",
        spot=spots[0],
    )
    session.add(r1)
    session.add(r2)
    session.flush()
    # put the session in the class that uses this fixture
    request.cls.session = session
    return session


@pytest.mark.usefixtures("session_with_demo_models")
class TestAllModelsTogether:
    def test_selecting_reservations(self, session_with_demo_models):
        result = session_with_demo_models.execute(
            select(Reservation).where(
                Reservation.date == DEMO_RESERVATION_DATE
            )
        )
        reservations = result.scalars().all()
        assert len(reservations) == 1
        logger.info(repr(reservations[0]))

        result = session_with_demo_models.execute(
            select(Reservation)
        )
        reservations = result.scalars().all()
        assert len(reservations) == 2
        logger.info(repr(reservations))

    def test_reservation_relationships(self, session_with_demo_models: Session):
        a_single_reservation = session_with_demo_models.execute(
            select(Reservation)
        ).scalars().first()

        assert a_single_reservation.spot.garage.workspace.slack_id == DEMO_WORKSPACE_SLACK_ID
