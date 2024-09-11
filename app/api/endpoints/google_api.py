from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.constaints import COLUMN_COUNT, GOOGLE_SHEET_URL, MINITMAL_ROW_COUNT
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
async def create_google_sheets_statistics(
        session: AsyncSession = Depends(get_async_session),
        kitty_report: Aiogoogle = Depends(get_service)
) -> str:
    """ superuser access only """
    completed_projects = (
        await charity_project_crud.get_projects_by_completion_rate(
            session
        )
    )
    row_count = len(completed_projects) + MINITMAL_ROW_COUNT
    spreadsheet_id = await spreadsheets_create(
        kitty_report,
        row_count,
        COLUMN_COUNT
    )
    await set_user_permissions(spreadsheet_id, kitty_report)
    await spreadsheets_update_value(
        spreadsheet_id, completed_projects, kitty_report,
        row_count, COLUMN_COUNT
    )
    return GOOGLE_SHEET_URL.format(spreadsheet_id=spreadsheet_id)
