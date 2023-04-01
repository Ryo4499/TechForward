import os
from glob import glob
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

__all__ = [
    os.path.split(os.path.splitext(file)[0])[1]
    for file in glob(os.path.join(os.path.dirname(__file__), "[a-zA-Z0-9]*.py"))
]

REGEX_PATTERN = r"^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$"
USERNAME_PATTERN = r"^[ぁ-ゖァ-ヾ一-鶴a-zA-Z0-9]+$"
PASSWORD_PATTERN = r"^[!-~]*$"

load_dotenv(verbose=True)

DATABASE = URL.create(
    drivername="mariadb+mariadbconnector",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    database=os.environ["DB_NAME"],
    port=os.environ["DB_PORT"],
)

ENGINE = create_engine(
    DATABASE,
    pool_recycle=60,
    pool_size=20,
    max_overflow=10,
)

# CONNECTIONの定義
CONNECTION = ENGINE.connect()
# scoped_session
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
metadata = MetaData()

Base = declarative_base(metadata=metadata)
Base.query = Session.query_property()
