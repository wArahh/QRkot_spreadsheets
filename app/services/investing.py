from datetime import datetime

from app.models.base import Funding


def donation_processing(
        target: Funding,
        sources: list[Funding]
) -> list[Funding]:
    update = []
    for source in [
        source for source in sources
        if source.full_amount > source.invested_amount
    ]:
        target.full_amount = target.full_amount or 0
        target.invested_amount = target.invested_amount or 0
        source.full_amount = source.full_amount or 0
        source.invested_amount = source.invested_amount or 0
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        target.invested_amount += transfer_amount
        source.invested_amount += transfer_amount
        datetime_now = datetime.utcnow()
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime_now
            update.append(source)
        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime_now
    return update
