"""pydantic models used in fastapi
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    plaintext_password: str


class User(UserBase):
    user_id: int
    user_role: int = 0

    class Config:
        orm_mode = True


class UserAndToken(BaseModel):
    user: User
    jwt: "Token"

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class BoardBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BoardCreate(BoardBase):
    pass


class PostBase(BaseModel):
    title: str = None
    message: str


class PostCreate(PostBase):
    board_name: str
    parent_id: Optional[int] = None
    file_id: Optional[int] = None


class Post(PostBase):
    post_id: int
    board: BoardBase
    date: str = None
    file: Optional["FileBase"] = None
    parent_id: Optional[int] = None
    children: list["Post"] = []
    latest_reply_date: Optional[str] = None
    user: Optional[User] = None

    class Config:
        orm_mode = True


class FileBase(BaseModel):
    file_id: int
    file_name: str
    file_hash: str
    content_type: str
    post_id: Optional[int] = None

    class Config:
        orm_mode = True


class Board(BoardBase):
    board_id: int
    posts: list[Post]

    class Config:
        orm_mode = True


class SearchListResponse(BaseModel):
    posts: list[Optional[Post]]
    boards: list[Optional[Board]]


class Requester(BaseModel):
    ip_address: str
    last_post_time: Optional[datetime] = None


class HealthCheckResponse(BaseModel):
    status: str
    time: datetime


Post.update_forward_refs()
UserAndToken.update_forward_refs()
