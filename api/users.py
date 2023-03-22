from typing import Optional, List

import fastapi
from fastapi import Path, Query
from pydantic import BaseModel

router = fastapi.APIRouter()

users = list()


class User(BaseModel):
    name: str
    is_active: bool
    bio: Optional[str]


@router.get("/users", response_model=List[User])
async def get_users():
    return users


@router.post("/users/{id}")
async def create_user(user: User):
    users.append(user)
    return "Success"


@router.get("/users/{ids}")
async def update_item(ids: int = Path(..., description="The id of the user you want to retrieve"),
                      q: str = Query(None, max_length=5)):
    return {"user": users[ids], "query": q}
