import enum
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DbCase(enum.Enum):
    inmem_testing = enum.auto()
    docker_testing = enum.auto()
    prod = enum.auto()

def get_session_for_case(case: DbCase) -> Session:
    if case == DbCase.inmem_testing:
        engine = create_engine('sqlite://')
        session = Session(bind=engine)
        return session
    elif case == DbCase.docker_testing:
        raise NotImplementedError("Docker session not implemented yet.")
    elif case == DbCase.prod:
        raise NotImplementedError("Prod session not implemented yet.")
    else:
        raise ValueError(f"Unknown case: {case}")
