from valet_parking_slack_bot.logic import ParkingSpotDesignator
from valet_parking_slack_bot.repo import ParkingSpotRepoBase
from unittest.mock import MagicMock, create_autospec

test_username = "test_user"

def test_reserve_spot_sanity():
    # arrange (given)
    repo = create_autospec(ParkingSpotRepoBase)
    repo.retrieve_available_spots.return_value = [1]
    designator = ParkingSpotDesignator(repo)
    
    # act (when)
    return_value = designator.try_reserve_spot(test_username)

    # assert (then)
    assert return_value
    repo.retrieve_available_spots.assert_called_once()
    repo.assign.assert_called_once_with(test_username, 1)


class TestReleaseByUsername:
    def test_one_reserved_spot(self):
        repo = create_autospec(ParkingSpotRepoBase)
        repo.retrieve_spots_by_user.return_value = '1'
        designator = ParkingSpotDesignator(repo)

        return_value = designator.release_by_username(test_username)
        assert return_value == "Parking spot 1 has been released successfully"

    def test_no_reserved_spots(self):
        repo = create_autospec(ParkingSpotRepoBase)
        repo.retrieve_spots_by_user.return_value = ''
        designator = ParkingSpotDesignator(repo)

        return_value = designator.release_by_username(test_username)
        assert return_value == "User had no assigned parking"

    def test_two_reserved_spots(self):
        repo = create_autospec(ParkingSpotRepoBase)
        repo.retrieve_spots_by_user.return_value = '1 2'
        designator = ParkingSpotDesignator(repo)

        return_value = designator.release_by_username(test_username)
        assert return_value == "You have several reserved spots: 1 2. Which one to release?"
