import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.constaints import (
    FORMAT, JSON_TEMLATE, MAX_GOOGLE_SHEET_CELL_COUNT, TOO_MUCH_CELL_ERROR
)
from app.core.config import settings
from app.utils import get_table_size


async def spreadsheets_create(
        kitty_report: Aiogoogle,
        charity_projects
) -> tuple:
    rows, columns = get_table_size(charity_projects)
    if (rows * columns) > (MAX_GOOGLE_SHEET_CELL_COUNT // columns):
        raise ValueError(
            TOO_MUCH_CELL_ERROR.format(
                all_rows_count=rows,
            )
        )
    service = await kitty_report.discover('sheets', 'v4')
    updated_template = copy.deepcopy(JSON_TEMLATE)
    grid_properties = (
        updated_template['sheets'][0]['properties']['gridProperties']
    )
    grid_properties['rowCount'] = rows
    grid_properties['columnCount'] = columns
    updated_template['sheets'][0]['properties']['title'] = (
        datetime.now().strftime(FORMAT)
    )
    response = await kitty_report.as_service_account(
        service.spreadsheets.create(json=updated_template)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


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
        table: list,
        kitty_report: Aiogoogle,
) -> None:
    rows, columns = get_table_size(table)
    await kitty_report.as_service_account(
        (
            await kitty_report.discover('sheets', 'v4')
        ).spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table
            }
        )
    )
