import logging
logger = logging.getLogger(__name__)
class ParkingSpotDesignator:
    def __init__(self, parking_spot_repo) -> None:
        self.parking_spot_repo = parking_spot_repo

    def spots(self):
        number_of_spots = len(self.parking_spot_repo.retrieve_available_spots())
        return number_of_spots

    def try_reserve_spot(self, user_id):
        available_spots: List[Any] = self.parking_spot_repo.retrieve_available_spots()
        if not available_spots:
            logger.info(f'No spots available for {user_id}')
            return None
        else:
            self.parking_spot_repo.assign(user_id, available_spots[0])
            logger.info(f'Spot {available_spots[0]} is assigned for {user_id}')
            return available_spots[0]

    def release_by_user_id(self, user_id):
        user_reserved_spots = self.parking_spot_repo.retrieve_spots_by_user(user_id)
        if len(user_reserved_spots) == 1:
            self.parking_spot_repo.release(user_reserved_spots[0])
            logger.info(f'Attempting to release spot {user_reserved_spots[0]}')
        logger.info(f'User {user_id} has several reserved spots: {user_reserved_spots}')
        return user_reserved_spots

    def release_by_spot_id(self, spot_id):
        self.parking_spot_repo.release(spot_id)
        return f"Parking spot {spot_id} has been released successfully"

        