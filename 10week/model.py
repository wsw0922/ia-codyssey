# model.py
from pydantic import BaseModel


class TodoItem(BaseModel):
    """Todo 항목을 나타내는 모델입니다."""

    task: str
    description: str