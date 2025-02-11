from sqlalchemy import select, update, delete, func
from models import async_session, Task, User
from pydantic import BaseModel, ConfigDict
from typing import List


class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int

    model_config = ConfigDict(from_attributes=True)

async def get_tasks(user_id: int):
    async with async_session as session:
        tasks = await session.scalars(select(Task).where(Task.user == user_id, Task.completed == False))

        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]

        return serialized_tasks
    

async def add_user(tg_id: int):
    async with async_session as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.id
        
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def get_completed_tasks(user_id):
    async with async_session as session:
        tasks = await session.scalar(select(func.count(Task.id)).where(Task.user == user_id, Task.completed == True))