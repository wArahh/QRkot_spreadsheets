from aiogoogle import Aiogoogle, AiogoogleError
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)
from app.utils import get_full_table

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    response_model=str,
)
async def create_google_sheets_statistics(
        session: AsyncSession = Depends(get_async_session),
        kitty_report: Aiogoogle = Depends(get_service)
):
    """ superuser access only """
    charity_projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    try:
        spreadsheet_id, spreadsheet_url = await spreadsheets_create(
            kitty_report,
            charity_projects
        )
    except AiogoogleError as e:
        raise e
    await set_user_permissions(
        spreadsheet_id,
        kitty_report
    )
    await spreadsheets_update_value(
        spreadsheet_id,
        get_full_table(charity_projects),
        kitty_report,
    )
    return spreadsheet_url
