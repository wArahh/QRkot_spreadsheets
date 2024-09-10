from sqlalchemy import Column, String, Text

from app.models.base import Funding


class CharityProject(Funding):
    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )

    def __repr__(self):
        return (
            f'<CharityProject({self.name=}, '
            f'{self.description[:20]=}), '
            f'{super().__repr__()}>'
        )
