import random
import logging
from abc import ABC
from typing import Any, Sequence

logger = logging.getLogger(__name__)

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

class ParkingSpotRepoStub(ParkingSpotRepoBase):
    """Stub for repo. Behaves semi-predictibly and only used for simple 
    integration testing. Not for production use!"""
    spots_db = ['1', '2', '3', 'grass']
    
    def retrieve_available_spots(self):
        logger.info("retrieving spots")
        return self.spots_db
    
    def retrieve_spots_by_user(self, username):
        logger.info(f"retriving spots for {username}")
        return random.choices(self.spots_db, k=1)

    def assign(self, username, spot_id):
        logger.info(f"assign spot {spot_id} to {username}")

    def release(self, spot_id):
        logger.info(f"releasing spot {spot_id}")
