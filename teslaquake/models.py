from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):

    # for streamlit ¯\_(ツ)_/¯
    __table_args__ = {'extend_existing': True}

    id: str = Field(primary_key=True)
    type: str
    place: Optional[str] = None
    time: datetime
    latitude: float
    longitude: float
    depth: Optional[float] = None
    magType: Optional[str] = None
    mag: Optional[float] = None
