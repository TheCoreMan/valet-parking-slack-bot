from abc import ABC
from typing import Any, Sequence

class ParkingSpotRepoBase(ABC):
    """Base class which defines the interface for Parking Spot Repositories."""

    # queries
    def retrieve_available_spots(self) -> Sequence[str]:
        raise NotImplementedError()

    def retrieve_spots_by_user(self, username: str) -> Sequence[str]:
        raise NotImplementedError()

    def assign(self, username: str, spot_id: str) -> None:
        raise NotImplementedError()

    def release(self, spot_id: str) -> None:
        raise NotImplementedError()
    