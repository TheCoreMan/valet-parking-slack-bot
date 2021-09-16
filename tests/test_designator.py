from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepo
from unittest.mock import MagicMock, create_autospec

def test_reserve_spot_sanity():
    # assume there are spots available
    repo = create_autospec(ParkingSpotRepo)
    designator = ParkingSpotDesignator(repo)
    assert designator.try_reserve_spot('test_user')
    # TODO test the actual assignation