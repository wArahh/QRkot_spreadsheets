from datetime import datetime

from app.models.base import Funding


def donation_processing(
        target: Funding,
        sources: list[Funding]
) -> list[Funding]:
    update = []
    for source in sources:
        remaining_target_amount = target.full_amount - target.invested_amount
        if remaining_target_amount <= 0:
            break
        transfer_amount = min(
            remaining_target_amount,
            source.full_amount - source.invested_amount
        )
        target.invested_amount += transfer_amount
        source.invested_amount += transfer_amount
        datetime_now = datetime.utcnow()
        for obj in (target, source):
            if obj.invested_amount >= obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime_now
                if obj is source:
                    update.append(obj)
    return update
