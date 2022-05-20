import uuid
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import os
from os.path import join, dirname
from dotenv import load_dotenv

REGEX_PATTERN = r"^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$"
USERNAME_PATTERN = r"^[ぁ-ゖァ-ヾ一-鶴a-zA-Z0-9]+$"
PASSWORD_PATTERN = r"^[!-~]*$"

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

DATABASE = "mariadb+mariadbconnector://%s:%s@%s/%s?charset=utf8mb4" % (
    os.environ.get("DB_USER"),
    os.environ.get("DB_PASS"),
    os.environ.get("DB_HOST"),
    os.environ.get("DB_NAME"),
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    pool_recycle=60,
    pool_size=20,
    max_overflow=10,
)

CONNECTION = ENGINE.connect()
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
metadata = MetaData(bind=ENGINE)

Base = declarative_base()
Base.query = Session.query_property()


def generate_uuid():
    return str(uuid.uuid4().hex)
