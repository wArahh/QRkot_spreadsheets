from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_kitty_report(
        session: AsyncSession = Depends(get_async_session),
        kitty_report: Aiogoogle = Depends(get_service)
):
    get_completed_projects = (
        await charity_project_crud.get_projects_by_completion_rate(
            session
        )
    )
    spreadsheetid = await spreadsheets_create(
        kitty_report, len(get_completed_projects)
    )
    await set_user_permissions(spreadsheetid, kitty_report)
    await spreadsheets_update_value(
        spreadsheetid, get_completed_projects, kitty_report
    )
    return get_completed_projects
