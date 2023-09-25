from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.schema import UUID


class DBBase(BaseModel):
    class Config:
        orm_mode = True


class Pagination(BaseModel):
    offset: int | None = Query(default=0, ge=0)
    limit: int | None = Query(default=100, ge=0)


class UUIDSchema(BaseModel):
    user_uuid: UUID = Field(example="72011ac8-7d60-4681-8f99-9775374f7266")


class IDSchema(BaseModel):
    id: int
