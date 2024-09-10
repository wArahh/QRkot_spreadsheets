from sqlalchemy import func, select
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

    @staticmethod
    async def get_projects_by_completion_rate(session: AsyncSession):
        closed_charity_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == 1
            ).order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )
        return closed_charity_projects.scalars().all()


charity_project_crud = CrudCharityProject(CharityProject)
