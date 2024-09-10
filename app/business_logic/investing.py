from datetime import datetime

from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import CertainDonationDB


def donation_processing(
        target: [CertainDonationDB, CharityProjectDB],
        sources: [list[CertainDonationDB], list[CharityProjectDB]]):
    objects_to_add = []
    if any(isinstance(source, list) for source in sources):
        sources = [item for sublist in sources for item in sublist]
    for source in sources:
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for item in (target, source):
            if source.fully_invested:
                break
            item.invested_amount += transfer_amount
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = datetime.utcnow()
        objects_to_add.extend([target, source])
    return objects_to_add
