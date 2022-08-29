from sqlmodel import SQLModel, create_engine

from config import TESLAQUAKE_DATABASE_URL, DEBUG

engine = create_engine(TESLAQUAKE_DATABASE_URL, echo=DEBUG)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
