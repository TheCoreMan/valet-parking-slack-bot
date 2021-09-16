from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepo
from unittest.mock import MagicMock, create_autospec

test_username = "test_user"

def test_reserve_spot_sanity():
    # arrange (given)
    repo = create_autospec(ParkingSpotRepo)
    repo.retrieve_available_spots.return_value = [1]
    designator = ParkingSpotDesignator(repo)
    
    # act (when)
    return_value = designator.try_reserve_spot(test_username)

    # assert (then)
    assert return_value
    repo.retrieve_available_spots.assert_called_once()
    repo.assign.assert_called_once_with(test_username, 1)