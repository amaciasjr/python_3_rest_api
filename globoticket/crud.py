from sqlalchemy import select
from sqlalchemy.orm import Session

from globoticket.models import DBEvent


def get_dbevent(id: int, db: Session) -> DBEvent | None:
    """
    Get single event from the database.
    """
    return db.get(DBEvent, id)


def get_all_dbevents(db: Session) -> list[DBEvent]:
    """
    Get all events from the database.
    """
    return db.execute(select(DBEvent)).scalars()
