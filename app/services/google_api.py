import copy
from datetime import datetime
from typing import Optional

from aiogoogle import Aiogoogle

from app.constaints import (
    BASE_ROW_COUNT, FORMAT, JSON_TEMLATE,
    MAX_GOOGLE_SHEET_CELL_COUNT, TABLE_HEADER,
    TOO_MUCH_CELL_ERROR
)
from app.core.config import settings
from app.utils import format_duration


async def spreadsheets_create(
        kitty_report: Aiogoogle,
        row_count: Optional[int],
        column_count: Optional[int]
):
    availabe_cells = MAX_GOOGLE_SHEET_CELL_COUNT // column_count
    all_rows_count = BASE_ROW_COUNT + row_count
    if all_rows_count > availabe_cells:
        raise ValueError(
            TOO_MUCH_CELL_ERROR.format(
                all_rows_count=all_rows_count, availabe_cells=availabe_cells
            )
        )
    service = await kitty_report.discover('sheets', 'v4')
    updated_template = copy.deepcopy(JSON_TEMLATE)
    (
        updated_template['sheets'][0]
        ['properties']['gridProperties']['rowCount']
    ) = all_rows_count
    (
        updated_template['sheets'][0]
        ['properties']['gridProperties']['columnCount']
    ) = column_count
    return await kitty_report.as_service_account(
        service.spreadsheets.create(json=JSON_TEMLATE)
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
    header_with_date = copy.deepcopy(TABLE_HEADER)
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
            range=f'R1C1:R{row_count + BASE_ROW_COUNT}C{column_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
