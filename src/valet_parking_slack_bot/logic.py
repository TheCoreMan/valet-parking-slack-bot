
class ParkingSpotDesignator:
    def __init__(self, parking_spot_repo) -> None:
        self.parking_spot_repo = parking_spot_repo


    def try_reserve_spot(self, username):
        available_spots = self.parking_spot_repo.retrieve_available_spots()
        if len(available_spots) == 0:
            return False
        else:
            self.parking_spot_repo.assign(username)
            return True

