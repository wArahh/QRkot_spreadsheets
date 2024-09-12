import copy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.constaints import (
    FORMAT, JSON_TEMLATE, MAX_GOOGLE_SHEET_CELL_COUNT, TOO_MUCH_CELL_ERROR,
    TABLE_HEADER
)
from app.core.config import settings
from app.utils import format_duration


def get_full_table(
    charity_projects
):
    formatted_rows = list(
        [
            charity_project.name,
            format_duration(
                charity_project.close_date - charity_project.create_date
            ),
            charity_project.description
        ]
        for charity_project in charity_projects
    )
    full_table = copy.deepcopy(TABLE_HEADER)
    full_table.extend(formatted_rows)
    full_table[0][1] = datetime.now().strftime(FORMAT)
    return full_table


def get_table_size(table):
    return len(table), max(map(len, table))


async def spreadsheets_create(
        kitty_report: Aiogoogle,
        google_table
) -> tuple:
    rows, columns = get_table_size(google_table)
    cell_count = rows * columns
    if cell_count > MAX_GOOGLE_SHEET_CELL_COUNT:
        raise ValueError(
            TOO_MUCH_CELL_ERROR.format(
                all_rows_count=cell_count,
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
