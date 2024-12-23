GET_OBJECT_ERROR = 'Во время вызова таблицы {model} проищошла ошибка: {error}'
DB_CHANGE_ERROR = (
    'При попытке изменения таблицы {model} '
    'в базе данных произошла ошибка: {error}'
)
NOT_IN_DB = 'Объект не найден в базе данных'
NAME_ALREADY_IN_USE = 'Это название уже занято'
CANNOT_DELETE_INVESTED_PROJECT = (
    'Нельзя удалять закрытый проект или проект, '
    'в который уже были инвестированы средства.'
)
CANNOT_UPDATE_FULLY_INVESTED_PROJECT = (
    'Нельзя редактировать закрытый проект или проект, '
    'в который уже были инвестированы средства.'
)
CANT_SET_LESS_THAN_ALREADY_DONATED = (
    'Нельзя изменить поле full_amount на значение меньше уже полученного'
)
INCORRECT_REGEX = 'Пароль содержит некорректные символы'
ACCEPTED_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
BEARER_TOKEN_URL = 'auth/jwt/login'
JWT_LIFETIME = 3600
AUTHENTICATION_BACKEND_NAME = 'jwt'
FORMAT = '%Y/%m/%d %H:%M:%S'
MAX_GOOGLE_SHEET_CELL_COUNT = 10_000_000
TOO_MUCH_CELL_ERROR = (
    'Превышено количество созднных ячек {created_cells_count} > ',
    MAX_GOOGLE_SHEET_CELL_COUNT
)
JSON_TEMLATE = (
    dict(
        properties=dict(
            title='KittyReport',
            locale='ru_RU'
        ),
        sheets=[
            dict(
                properties=dict(
                    sheetType='GRID',
                    sheetId=0,
                    title=None,
                    gridProperties=dict(
                        rowCount=None,
                        columnCount=None,
                    )
                )
            )
        ]
    )
)
TABLE_HEADER = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
SPREADSHEET_CREATE_ERROR = 'Error creating spreadsheet: {error}'
