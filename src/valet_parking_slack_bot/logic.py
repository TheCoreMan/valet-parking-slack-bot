
class ParkingSpotDesignator:
    def __init__(self, parking_spot_repo) -> None:
        self.parking_spot_repo = parking_spot_repo


    def try_reserve_spot(self, username):
        available_spots = self.parking_spot_repo.retrieve_available_spots()
        if len(available_spots) == 0:
            return False
        else:
            self.parking_spot_repo.assign(username, available_spots[0])
            return True

    def release_by_username(self, username):
        user_reserved_spots = self.parking_spot_repo.retrieve_spots_by_user(username)
        if len(user_reserved_spots) == 0:
            return "User had no assigned parking"
        elif len(user_reserved_spots) == 1:
            self.parking_spot_repo.release(user_reserved_spots[0])
            return f"Parking spot {user_reserved_spots[0]} has been released successfully"
        else:
            return f"You have several reserved spots: {user_reserved_spots}. Which one to release?"

    #TODO add user validation for releasing spots?
    def release_by_spot_id(self, spot_id):
        self.parking_spot_repo.release(spot_id)
        return f"Parking spot {spot_id} has been released successfully"

        