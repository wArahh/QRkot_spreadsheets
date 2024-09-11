from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import (
    CANNOT_DELETE_INVESTED_PROJECT, CANNOT_UPDATE_FULLY_INVESTED_PROJECT,
    CANT_SET_LESS_THAN_ALREADY_DONATED, NAME_ALREADY_IN_USE
)
from app.crud import charity_project_crud
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    if await charity_project_crud.get_charity_project_by_name(
            charity_project_name,
            session
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_ALREADY_IN_USE
        )


async def validate_charity_project_update(
        project_id: int,
        charity_project: CharityProjectUpdate,
        session: AsyncSession
) -> None:
    db_project = await charity_project_crud.get(project_id, session)
    await check_name_duplicate(charity_project.name, session)
    if db_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CANNOT_UPDATE_FULLY_INVESTED_PROJECT
        )
    if (
        charity_project.full_amount is not None and
            db_project.invested_amount > charity_project.full_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CANT_SET_LESS_THAN_ALREADY_DONATED
        )


async def validate_charity_project_delete(
        project_id: int,
        session: AsyncSession
):
    if (
        await charity_project_crud.get(project_id, session)
    ).invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CANNOT_DELETE_INVESTED_PROJECT
        )
