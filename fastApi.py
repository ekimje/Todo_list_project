from fastApi import FastApi, HttpException
from pydantic import BaseModel
from typing import Optimal, List
from uuid import UUID, uuid4

from models import TodoItem
from storage import Todostorage

app = FastApi()

class TodoCreate(BaseModel):
    id:Optimal[UUID] = uuid4()
    