from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.models import Donation


class CrudDonation(CrudBase):
    @staticmethod
    async def get_user_donations(
            user_id: int,
            session: AsyncSession,
    ):
        get_user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        return get_user_donations.scalars().all()


donation_crud = CrudDonation(Donation)
