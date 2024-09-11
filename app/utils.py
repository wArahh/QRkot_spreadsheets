from datetime import timedelta

from app.constaints import BASE_COLUMN_COUNT, BASE_ROW_COUNT


def format_duration(delta: timedelta) -> str:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    day_label = "day" if days == 1 else "days"
    return (
        f"{days} "
        f"{day_label} "
        f"{hours}"
        f":{minutes}"
        f":{seconds}"
        f".{milliseconds}"
    )


def calculate_dimensions(data: list[dict]) -> (int, int):
    if not data:
        return BASE_ROW_COUNT, BASE_COLUMN_COUNT
    return len(data) + BASE_ROW_COUNT, BASE_COLUMN_COUNT
