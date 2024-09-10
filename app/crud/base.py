from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import (
    CANNOT_DELETE_INVESTED_PROJECT,
    CANNOT_UPDATE_FULLY_INVESTED_PROJECT,
    CANT_SET_LESS_THAN_ALREADY_DONATED,
    NOT_IN_DB, DB_CHANGE_ERROR
)
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
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=NOT_IN_DB
            )
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
            obj,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_data = obj.dict()
        if user is not None:
            obj_data['user_id'] = user.id
        return await self.db_change(self.model(**obj_data), session)

    async def update(
            self,
            db_obj_id: int,
            obj,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        if db_obj.fully_invested == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANNOT_UPDATE_FULLY_INVESTED_PROJECT
            )
        if db_obj.invested_amount > obj.full_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANT_SET_LESS_THAN_ALREADY_DONATED
            )
        update_data = obj.dict(exclude_unset=True)
        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.db_change(db_obj, session)

    async def delete(
            self,
            db_obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await self.get(db_obj_id, session)
        if db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=CANNOT_DELETE_INVESTED_PROJECT
            )
        return await self.db_change(db_obj, session, delete=True)

    @staticmethod
    async def get_available_investments(
            db_model,
            session: AsyncSession,
    ):
        available_investments = await session.execute(
            select(db_model).where(
                db_model.fully_invested == 0
            ).order_by(db_model.create_date)
        )
        return available_investments.scalars().all()

    @staticmethod
    async def db_change(
            obj,
            session: AsyncSession,
            delete=False,
            add_list=None
    ):
        try:
            if delete:
                await session.delete(obj)
                await session.commit()
            else:
                if add_list:
                    session.add_all(add_list)
                else:
                    session.add(obj)
                await session.commit()
                await session.refresh(obj)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=DB_CHANGE_ERROR
            )
        return obj
