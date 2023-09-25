from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
JoinedModelType = TypeVar("JoinedModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self, model: Type[ModelType], joined_model: Type[JoinedModelType] | None = None
    ):
        self.model = model
        self.joined_model = joined_model

    async def get(self, session: AsyncSession, id: int) -> ModelType:

        if self.joined_model:
            mapper = inspect(self.model).mapper

            for rel in mapper.relationships:
                key = rel.key
                rel_name = key

            query = (
                select(self.model)
                .join(self.joined_model)
                .options(joinedload(rel_name))
                .where(self.model.id == id)
            )

        else:
            query = select(self.model).where(self.model.id == id)

        item = await session.execute(query)
        return item.scalars().one_or_none()

    async def get_multi(
        self,
        offset: int | None,
        limit: int | None,
        session: AsyncSession,
        filters: dict | None = None,
    ) -> list[ModelType]:
        query = select(self.model)

        if filters:
            filter_conditions = []
            for field, value in filters.items():
                filter_conditions.append(getattr(self.model, field) == value)
            query = query.filter(and_(*filter_conditions))

        query = query.offset(offset).limit(limit)

        items = await session.execute(query)
        return items.scalars().all()

    async def create(
        self, session: AsyncSession, *, data: CreateSchemaType
    ) -> ModelType:
        item = self.model(**data.dict())
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def update(
        self, session: AsyncSession, *, item: ModelType, data: UpdateSchemaType | dict
    ) -> ModelType:

        if isinstance(data, dict):
            updated_data = data
        else:
            updated_data = data.dict(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(item, field, value)

        session.add(item)
        await session.commit()
        await session.refresh(item)

        return item

    async def remove(self, session: AsyncSession, *, id: int) -> ModelType:
        item = session.query(self.model).get(id)
        await session.delete(item)
        await session.commit()

        return item
