from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.constaints import BASE_COLUMN_COUNT, BASE_ROW_COUNT
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)
from app.utils import calculate_dimensions

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
    completed_projects = (
        await charity_project_crud.get_projects_by_completion_rate(
            session
        )
    )
    row_count, column_count = calculate_dimensions(completed_projects)
    spreadsheet = await spreadsheets_create(
        kitty_report,
        row_count,
        column_count
    )
    await set_user_permissions(
        spreadsheet['spreadsheetId'],
        kitty_report
    )
    await spreadsheets_update_value(
        spreadsheet['spreadsheetId'],
        completed_projects,
        kitty_report,
        row_count,
        column_count
    )
    return spreadsheet['spreadsheetUrl']
