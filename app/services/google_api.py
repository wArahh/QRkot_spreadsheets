import copy
from datetime import datetime
from typing import Optional

from aiogoogle import Aiogoogle

from app.constaints import (FORMAT, JSON_TEMLATE, MAX_GOOGLE_SHEET_CELL_COUNT,
                            TOO_MUCH_CELL_ERROR)
from app.core.config import settings


async def spreadsheets_create(
        kitty_report: Aiogoogle,
        row_count: Optional[int],
        column_count: Optional[int]
) -> tuple:
    available_cells_count = MAX_GOOGLE_SHEET_CELL_COUNT // column_count
    if row_count > available_cells_count:
        raise ValueError(
            TOO_MUCH_CELL_ERROR.format(
                all_rows_count=row_count, availabe_cells=available_cells_count
            )
        )
    service = await kitty_report.discover('sheets', 'v4')
    updated_template = copy.deepcopy(JSON_TEMLATE)
    grid_properties = (
        updated_template['sheets'][0]['properties']['gridProperties']
    )
    grid_properties['rowCount'] = row_count
    grid_properties['columnCount'] = column_count
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
        row_count: Optional[int],
        column_count: Optional[int]
) -> None:
    formatted_table = [[str(cell) for cell in row] for row in table]
    formatted_table[0][1] = datetime.now().strftime(FORMAT)
    await kitty_report.as_service_account(
        (
            await kitty_report.discover('sheets', 'v4')
        ).spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': formatted_table
            }
        )
    )
