from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(None)
    full_amount: int = Field(ge=1)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(max_length=100)
    description: Optional[str] = Field()
    full_amount: Optional[int] = Field(1, ge=1)


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = Field(False)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
