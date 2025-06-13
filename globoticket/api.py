"""
api.py
---

The REST Api for the Globoticket events database.
"""
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from globoticket.crud import get_all_dbevents, get_dbevent
from globoticket.database import SessionLocal
from globoticket.models import DBEvent
from globoticket.schemas import Event

app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent


def get_session() -> Session:
    """
    Get a database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/event/{id}", response_model=Event)
def get_event(id: int, session: Annotated[Session, Depends(get_session)]) -> DBEvent:
    """
    Get an event by id.
    """
    event = get_dbevent(id, session)
    if event is None:
        raise HTTPException(status_code=404, detail=f"No product with id {id}")
    return event


@app.get("/event/", response_model=list[Event])
def get_all_events(session: Annotated[Session, Depends(get_session)]) -> list[DBEvent]:
    """
    Get all events.
    """
    return get_all_dbevents(session)


# This should come AFTER all other endpoints
app.mount("/", StaticFiles(directory=PROJECT_ROOT / "static", html=True))
