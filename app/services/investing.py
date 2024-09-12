from datetime import datetime

from app.models.base import Funding


def donation_processing(
        target: Funding,
        sources: list[Funding]
) -> list[Funding]:
    update = []
    datetime_now = datetime.utcnow()
    for source in sources:
        update.append(source)
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += transfer_amount
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime_now
    return update
