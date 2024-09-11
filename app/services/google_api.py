from datetime import datetime
from typing import Optional

from aiogoogle import Aiogoogle
from aiogoogle.excs import AiogoogleError
from fastapi import HTTPException, status

from app.constaints import (
    FORMAT, JSON_TEMLATE, MAX_GOOGLE_SHEET_CELL_COUNT,
    TABLE_HEADER, TOO_MUCH_CELL_ERROR
)
from app.core.config import settings
from app.utils import format_duration


async def spreadsheets_create(
        kitty_report: Aiogoogle,
        row_count: Optional[int],
        column_count: Optional[int]
) -> str:
    try:
        availabe_cells = MAX_GOOGLE_SHEET_CELL_COUNT // column_count
        if row_count > availabe_cells:
            raise ValueError(
                TOO_MUCH_CELL_ERROR.format(
                    cell_difference=row_count - availabe_cells,
                )
            )
        service = await kitty_report.discover('sheets', 'v4')
        if row_count is not None:
            JSON_TEMLATE['sheets'][0]['properties']['gridProperties'][
                'rowCount'
            ] = row_count
        if column_count is not None:
            JSON_TEMLATE['sheets'][0]['properties']['gridProperties'][
                'columnCount'
            ] = column_count
        response = await kitty_report.as_service_account(
            service.spreadsheets.create(json=JSON_TEMLATE)
        )
        return response['spreadsheetId']
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except AiogoogleError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def set_user_permissions(
        spreadsheet_id: str,
        kitty_report: Aiogoogle
) -> None:
    service = await kitty_report.discover('drive', 'v3')
    await kitty_report.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        kitty_report: Aiogoogle,
        row_count: Optional[int],
        column_count: Optional[int]
) -> None:
    service = await kitty_report.discover('sheets', 'v4')
    header_with_date = [row[:] for row in TABLE_HEADER]
    header_with_date[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *header_with_date,
        *list(
            [
                str(charity_project.name),
                str(
                    format_duration(
                        charity_project.close_date -
                        charity_project.create_date
                    )
                ),
                str(charity_project.description)
            ] for charity_project in charity_projects
        )
    ]
    await kitty_report.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
