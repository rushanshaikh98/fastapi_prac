from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from api.utils.courses import get_user_courses
from api.utils.users import get_user, get_users, get_user_by_email, create_user
from db.db_setup import get_db, async_get_db
from pydantic_schemas.courses import Course
from pydantic_schemas.users import User, UserCreate

router = fastapi.APIRouter()


@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/{id}", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered!")
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not found!")
    return db_user


@router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_courses = get_user_courses(db=db, user_id=user_id)
    if not db_courses:
        raise HTTPException(status_code=404, detail="Courses Not found!")
    return db_courses

