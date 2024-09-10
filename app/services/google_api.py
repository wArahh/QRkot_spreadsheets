from aiogoogle import Aiogoogle

from app.constaints import COLUMNCOUNT, DATETIME_NOW, MINITMAL_ROW_COUNT
from app.core.config import settings
from app.utils import format_duration


async def spreadsheets_create(kitty_report: Aiogoogle, column_count) -> str:
    service = await kitty_report.discover('sheets', 'v4')
    response = await kitty_report.as_service_account(
        service.spreadsheets.create(
            json={
                'properties': {
                    'title': f'Отчёт от {DATETIME_NOW}',
                    'locale': 'ru_RU'
                },
                'sheets': [
                    {
                        'properties': {
                            'sheetType': 'GRID',
                            'sheetId': 0,
                            'title': 'KittyReport',
                            'gridProperties': {
                                'rowCount': MINITMAL_ROW_COUNT + column_count,
                                'columnCount': COLUMNCOUNT
                            }
                        }
                    }
                ]
            }
        )
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        kitty_report: Aiogoogle
) -> None:
    service = await kitty_report.discover('drive', 'v3')
    await kitty_report.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json={
                'type': 'user',
                'role': 'writer',
                'emailAddress': settings.email
            },
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        kitty_report: Aiogoogle
) -> None:
    service = await kitty_report.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', DATETIME_NOW],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for charity_project in charity_projects:
        table_values.append(
            [
                str(charity_project.name),
                str(
                    format_duration(
                        charity_project.close_date -
                        charity_project.create_date
                    )
                ),
                str(charity_project.description)
            ]
        )
    await kitty_report.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
