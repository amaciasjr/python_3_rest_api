from datetime import date

import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from globoticket.api import app, get_session
from globoticket.models import Base, DBCategory, DBEvent

test_db = sqlalchemy.create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=True,
)

test_sessionmaker = sessionmaker(bind=test_db)


def setup_test_db():
    Base.metadata.create_all(test_db)
    session = Session(test_db)
    cat = DBCategory(name="t")
    ev = DBEvent(
        product_code="123456",
        date=date(2024, 1, 1),
        price=5.50,
        category=cat,
    )
    session.add(cat)
    session.add(ev)
    session.commit()


def get_test_session():
    setup_test_db()
    session = test_sessionmaker()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_db)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    del app.dependency_overrides[get_session]
