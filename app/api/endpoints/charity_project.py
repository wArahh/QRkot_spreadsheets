from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validatiors import (
    check_name_duplicate,
    validate_charity_project_delete,
    validate_charity_project_update
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import donation_processing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """ superuser access only """
    await check_name_duplicate(charity_project.name, session)
    target = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    session.add_all(
        donation_processing(
            target,
            await donation_crud.get_available_investments(
                session
            )
        )
    )
    await session.commit()
    await session.refresh(target)
    return target


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        charity_project: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """ superuser access only """
    await validate_charity_project_update(project_id, charity_project, session)
    return await charity_project_crud.update(
        project_id,
        charity_project,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """ superuser access only """
    await validate_charity_project_delete(project_id, session)
    return await charity_project_crud.delete(
        project_id,
        session
    )
