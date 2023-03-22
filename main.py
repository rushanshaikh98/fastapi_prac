from typing import Optional, List

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

users = list()


class User(BaseModel):
    name: str
    is_active: bool
    bio: Optional[str]


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/users/{id}")
async def create_user(user: User):
    users.append(user)
    return "Success"


@app.get("/users/{ids}")
async def update_item(ids: int = Path(..., description="The id of the user you want to retrieve"),
                      q: str = Query(None, max_length=5)):
    return {"user": users[ids], "query": q}
