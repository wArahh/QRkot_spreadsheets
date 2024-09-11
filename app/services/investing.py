from datetime import datetime

from app.models.base import Funding


def donation_processing(
        target: [Funding],
        sources: list[Funding]
) -> list[Funding]:
    objects_to_update = []
    for source in sources:
        if source.fully_invested:
            break
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        target.invested_amount += transfer_amount
        source.invested_amount += transfer_amount
        if source.invested_amount == source.full_amount:
            datetime_now = datetime.utcnow()
            source.fully_invested = True
            target.fully_invested = True
            source.close_date = datetime_now
            target.close_date = datetime_now
        objects_to_update.append(source)
    return objects_to_update
