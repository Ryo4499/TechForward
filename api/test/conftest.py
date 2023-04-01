import pytest
from typing import Union
from entities import add_test_data
from entities.tag import Tag
from entities.comment import Comment
from entities.article import Article
from entities.user import User
from flask import Flask
from run import create_app


@pytest.fixture(scope="session")
def app() -> Flask:
    return create_app("config.Testing")


@pytest.fixture(scope="session")
def test_data() -> dict[str, list[Union[Article, Comment, Tag, User]]]:
    return add_test_data()
