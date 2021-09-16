class ParkingSpotRepo():
    def __init__(self) -> None:
        pass

    def retrieve_available_spots(self):
        raise NotImplementedError()

    def assign(self, username, parking_spot):
        raise NotImplementedError()