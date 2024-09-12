from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Funding
from app.models.user import User


class CrudBase:
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        get_object = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        obj = get_object.scalars().first()
        return obj

    async def get_all(
            self,
            session: AsyncSession,
    ):
        get_all = await session.execute(
            select(self.model)
        )
        return get_all.scalars().all()

    async def create(
            self,
            obj: Funding,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ):
        obj_data = obj.dict()
        if user is not None:
            obj_data['user_id'] = user.id
        new_obj = self.model(**obj_data)
        session.add(new_obj)
        if commit:
            await session.commit()
            await session.refresh(new_obj)
        return new_obj

    async def update(
            self,
            db_obj_id: int,
            obj,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        update_data = obj.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db_obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get_available_investments(
            db_model,
            session: AsyncSession,
    ):
        return (
            await session.execute(
                select(
                    db_model
                ).where(
                    db_model.fully_invested == 0
                ).order_by(
                    db_model.create_date
                )
            )
        ).scalars().all()
