import os
from datetime import datetime
from tempfile import NamedTemporaryFile

import pytest
from fastapi.testclient import TestClient

from twok.api import app
from twok.api.dependencies import Auth
from twok.database import models
from twok.database.crud import DB
from twok.database.session import Session


@pytest.fixture(scope="function")
def client(env):
    yield TestClient(app)


@pytest.fixture(scope="function")
def db(env):
    pool = Session()
    db_session = pool.get_session()

    db = DB(session=db_session)
    try:
        yield db
    finally:
        db_session.close()
        del db


@pytest.fixture(scope="function")
def env():
    os.environ["JWT_SECRET_KEY"] = "secret"
    # create a temporary file to use as the database
    with NamedTemporaryFile() as temp:
        os.environ["DATABASE_URL"] = f"sqlite:///{temp.name}"
        yield


@pytest.fixture(scope="function")
def create_user(db: DB):
    yield db.user.create(
        name="username",
        password_hash="$2b$12$Tlj5xnuVKIWlE319Bu81ce8YRsWt5.Q/dkiQMgkdBbTJSFNPtzlzy",
        email_address="user@example.com",
    )


# create jwt access token for user
@pytest.fixture(scope="function")
def create_token(db: DB, create_user: models.User):
    user = db.user.get("username")
    auth = Auth(db)
    token = auth.create_access_token(data={"sub": user.name})
    return token


@pytest.fixture(scope="function")
def create_board(db: DB):
    yield db.board.create(
        name="board",
    )


@pytest.fixture(scope="function")
def create_post(db: DB, create_board: models.Board):
    yield db.post.create(
        title="Test Message Title",
        message="Test Message",
        board_id=create_board.board_id,
        date=datetime.now(),
    )


@pytest.fixture(scope="function")
def create_file(db: DB, create_post: models.Post):
    yield db.file.create(
        file_name="the_metamorphosis.jpg",
        file_hash="aff4996afe18fa33760ea1eb463f6fa71f8b01f251ef7e969e9c3b21c7a5cbc8",
        post_id=create_post.post_id,
        content_type="image/jpeg",
    )
