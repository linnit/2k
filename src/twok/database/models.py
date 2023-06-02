"""sqlalchemy models
"""
from sqlalchemy.orm import relationship
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
)
from sqlalchemy.schema import UniqueConstraint

from twok.database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password_hash = Column(String(128))

    # user_role column defaults to 0
    # 0 = user
    # 1 = admin
    user_role = Column(Integer, default=0)

    # posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.user_id"))
    user = relationship("User", backref="posts")
    title = Column(String(128), nullable=True)
    message = Column(String(512), nullable=True)
    date = Column(String(32), nullable=True)

    board_id = Column(ForeignKey("board.board_id"))
    board = relationship("Board", back_populates="posts")

    parent_id = Column(Integer, ForeignKey("post.post_id"), index=True, nullable=True)
    parent = relationship("Post", backref="children", remote_side=[post_id])

    latest_reply_date = Column(String(32), nullable=True)

    file = relationship("File", back_populates="post", uselist=False)


class Board(Base):
    __tablename__ = "board"

    board_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    posts = relationship("Post", back_populates="board")


class File(Base):
    __tablename__ = "file"

    file_id = Column(Integer, primary_key=True)
    file_name = Column(String(128), nullable=False)
    file_hash = Column(String(128), nullable=False)
    content_type = Column(String(64), nullable=False)  # mimetype
    post_id = Column(Integer, ForeignKey("post.post_id"))
    post = relationship("Post", back_populates="file")


class Requester(Base):
    __tablename__ = "requester"

    requester_id = Column(Integer, primary_key=True)
    ip_address = Column(String(64), nullable=False)
    last_post_time = Column(String(32), nullable=False)
