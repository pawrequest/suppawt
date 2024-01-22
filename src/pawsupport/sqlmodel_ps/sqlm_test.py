import pytest
from sqlmodel import create_engine, SQLModel, Session, StaticPool


@pytest.fixture(scope="function")
def engine_fxt():
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)


@pytest.fixture(scope="session")
def session_fxt():
    # engine = engine_fxt
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

