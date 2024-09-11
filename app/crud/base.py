from typing import Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constaints import (
    CANNOT_DELETE_INVESTED_PROJECT, CANNOT_UPDATE_FULLY_INVESTED_PROJECT,
    CANT_SET_LESS_THAN_ALREADY_DONATED, DB_CHANGE_ERROR, NOT_IN_DB
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
        new_obj = self.model(**obj_data)
        try:
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=DB_CHANGE_ERROR.format(
                    model=self.model.__name__,
                    error=e
                )
            )
        return new_obj

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
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

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
        try:
            await session.delete(db_obj)
            await session.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=DB_CHANGE_ERROR.format(
                    model=self.model.__name__,
                    error=DB_CHANGE_ERROR.format(
                        model=self.model.__name__,
                        error=DB_CHANGE_ERROR.format()
                    )
                )
            )
        return db_obj

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
