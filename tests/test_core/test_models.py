import pytest
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from server.core.models import Base


@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module")
def session(engine):
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    return session


class TestModel(Base):
    name = Column(String)


class Account(Base):
    name = Column(String)


def test_table_name():
    assert TestModel.__tablename__ == "test_models"


def test_default_values(session):
    test_record = TestModel(name="Test")
    session.add(test_record)
    session.commit()

    record = session.get(TestModel, test_record.id)
    assert record.created_at is not None
    assert record.last_updated_at is None
    assert record.delete_at is None
    assert record.revision_id == 1


def test_foreign_key_relationships(session):
    account = Account(name="Test Account")
    session.add(account)
    session.commit()

    test_record = TestModel(name="Test", creator_id=account.id)
    session.add(test_record)
    session.commit()

    assert test_record.creator_id == account.id


def test_revision_id_increment(session):
    test_record = TestModel(name="Test")
    session.add(test_record)
    session.commit()

    initial_revision_id = test_record.revision_id

    test_record.name = "Updated Test"
    session.commit()

    updated_record = session.get(TestModel, test_record.id)
    assert updated_record.revision_id == initial_revision_id + 1
