from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.models import CharityProject


class CrudCharityProject(CrudBase):
    @staticmethod
    async def get_charity_project_by_name(
            charity_name: str,
            session: AsyncSession,
    ):
        get_charity_project_name = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_name
            )
        )
        return get_charity_project_name.scalars().first()


charity_project_crud = CrudCharityProject(CharityProject)
