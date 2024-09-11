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
        return (
            await session.execute(
                select(
                    CharityProject
                ).filter(
                    CharityProject.name == charity_name
                )
            )
        ).scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(session: AsyncSession):
        return (
            await session.execute(
                select(CharityProject).where(
                    CharityProject.fully_invested == 1
                ).order_by(
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                )
            )
        ).scalars().all()


charity_project_crud = CrudCharityProject(CharityProject)
