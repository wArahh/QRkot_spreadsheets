from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import CharityProject
from app.models.user import User
from app.schemas.donation import CertainDonationDB, CreateDonation, DonationDB
from app.services import donation_processing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
) -> list[DonationDB]:
    """ superuser access only """
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=list[CertainDonationDB],
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> list[CertainDonationDB]:
    return await donation_crud.get_user_donations(user.id, session)


@router.post(
    '/',
    response_model=CertainDonationDB,
)
async def create_donation(
        donation: CreateDonation,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
) -> CertainDonationDB:
    target = await donation_crud.create(
        donation, session, user
    )
    session.add_all(
        donation_processing(
            target,
            await donation_crud.get_available_investments(
                CharityProject, session
            )
        )
    )
    await session.commit()
    await session.refresh(target)
    return target
