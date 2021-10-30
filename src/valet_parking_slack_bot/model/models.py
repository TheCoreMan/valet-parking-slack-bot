import enum
from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import (
    Boolean, 
    Column, 
    DateTime, 
    Enum, 
    ForeignKey, 
    Integer, 
    String,
)

# See https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#setting-up-the-registry
mapper_registry = registry()
Base = mapper_registry.generate_base()


@enum.unique
class PricingTier(enum.Enum):
    free = enum.auto()
    paid = enum.auto()


TABLE_NAME_WORKSPACES = "workspaces"
TABLE_NAME_SPOTS = "spots"
TABLE_NAME_GARAGES = "garages"
TABLE_NAME_USERS = "users"
TABLE_NAME_RESERVATIONS = "reservations"


class Workspace(Base):
    __tablename__ = TABLE_NAME_WORKSPACES
    id = Column(Integer, primary_key=True)
    slack_id = Column(String)
    name = Column(String)
    pricing_tier = Column(Enum(PricingTier), nullable=False)
    onboard_time = Column(DateTime)

    # Setting up Relationships: See
    # https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#orm-tutorial-relationship
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#relationship-patterns
    # for details.
    
    # workspace --[1..n]-> garages
    garages = relationship(
        "Garage",
        back_populates="workspace",
    )
    # workspace -[1]--[0..n]-> users
    users = relationship(
        "User",
        back_populates="workspace",
    )

    def __repr__(self):
        # TODO add emoji to repr
        return f"Workspace({self.id=}, {self.name=}, {self.pricing_tier=}, {self.onboard_time=})"


class Garage(Base):
    __tablename__ = TABLE_NAME_GARAGES
    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_instructions = Column(String)
    arrival_instructions = Column(String)
    
    # Garage <-[n..1]-- workspace
    workspace_id = Column(
        String, 
        ForeignKey(f'{TABLE_NAME_WORKSPACES}.id'),
    )
    workspace = relationship(
        "Workspace",
        back_populates=TABLE_NAME_GARAGES,
    )

    # Garage --[1..n]-> spots
    spots = relationship(
        "Spot",
        back_populates="garage",
    )

    def __repr__(self):
        return f"Garage {self.name} at {repr(self.workspace)}"


class Spot(Base):
    __tablename__ = TABLE_NAME_SPOTS
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    attributes = Column(String, nullable=True)
    
    # Spot <-[n..1]-- garage
    garage_id = Column(
        String,
        ForeignKey(f"{TABLE_NAME_GARAGES}.id"),
    )
    garage = relationship(
        "Garage",
        back_populates=TABLE_NAME_SPOTS
    )

    # Spot -[1]--[1..n]-> reservations
    reservations = relationship(
        "Reservation",
        back_populates="spot",
    )

    def __repr__(self):
        return f"Spot {self.name} at {self.garage}"


# TODO use this somehow?
#class SpotAttributes(enum.Enum):
#    accessible = enum.auto()
#    charger = enum.auto()
#    scooter = enum.auto()
#    wide = enum.auto()

class User(Base):
    __tablename__ = TABLE_NAME_USERS
    id = Column(Integer, primary_key=True)
    slack_id = Column(String)
    name = Column(String)
    # Which garage to give this user by default? The ID of the garage.
    default_garage = Column(String, nullable=True)
    spot_preferences = Column(String)
    spot_requirements = Column(String)

    # Workspace --[1..n]-> User
    workspace_id = Column(
        String, 
        ForeignKey(f'{TABLE_NAME_WORKSPACES}.id'),
    )
    workspace = relationship(
        "Workspace", 
        back_populates=TABLE_NAME_USERS,
    )


class Reservation(Base):
    __tablename__ = TABLE_NAME_RESERVATIONS
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False)
    member_id = Column(String, nullable=False)
    member_name = Column(String)
    
    # Reservation -[1]--[n]-> spot (multiple reservations can be made for the 
    # same spot, on different dates).
    spot_id = Column(
        Integer,
        ForeignKey(f'{TABLE_NAME_SPOTS}.id'),
    )
    spot = relationship(
        "Spot",
        back_populates=TABLE_NAME_RESERVATIONS,
    )

    def __repr__(self):
        return f"Reservation: \
{'Active' if self.active else 'Inactive'} \
by {self.member_id} \
({self.member_name if self.member_name else 'unknown name'}) \
for {self.date} spot {repr(self.spot)}"

def create_all_tables(session: Session):
    Base.metadata.create_all(session.get_bind())