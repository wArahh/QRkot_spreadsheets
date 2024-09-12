from datetime import datetime, timedelta

from app.constaints import FORMAT, TABLE_HEADER


def format_duration(delta: timedelta) -> str:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    day_label = 'day' if days == 1 else 'days'
    return (
        f'{days} '
        f'{day_label} '
        f'{hours}'
        f':{minutes}'
        f':{seconds}'
        f'.{milliseconds}'
    )


def get_full_table(
    charity_projects
):
    formatted_table = [
        [str(cell) for cell in row]
        for row in (
            TABLE_HEADER + list(
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
        )
    ]
    formatted_table[0][1] = datetime.now().strftime(FORMAT)
    return formatted_table


def get_table_size(table):
    return len(table), max(len(row) for row in TABLE_HEADER)
