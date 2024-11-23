"""
    Contains global database logic
    Sets up connection to database
"""
from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = 'sqlite:///./db.sql'

connect_args = {'check_same_thread': False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    """ build all database models """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """ Get db connection session """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]