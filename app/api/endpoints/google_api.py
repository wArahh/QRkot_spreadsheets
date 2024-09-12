from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import SPREADSHEET_CREATE_ERROR, TABLE_HEADER
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from app.utils import format_duration

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
    full_table = TABLE_HEADER + [
        [
            str(charity_project.name),
            str(
                format_duration(
                    charity_project.close_date -
                    charity_project.create_date
                )
            ),
            str(charity_project.description)
        ] for charity_project in (
            await charity_project_crud.get_projects_by_completion_rate(
                session
            )
        )
    ]
    row_count, column_count = (
        len(full_table), max(len(row) for row in TABLE_HEADER)
    )
    try:
        spreadsheet_id, spreadsheet_url = await spreadsheets_create(
            kitty_report,
            row_count,
            column_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SPREADSHEET_CREATE_ERROR.format(error=e)
        )
    await set_user_permissions(
        spreadsheet_id,
        kitty_report
    )
    await spreadsheets_update_value(
        spreadsheet_id,
        full_table,
        kitty_report,
        row_count,
        column_count
    )
    return spreadsheet_url
