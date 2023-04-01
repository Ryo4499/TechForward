from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import *
from sqlalchemy.sql.functions import current_timestamp
from . import Base
from .utils import generate_uuid


# TokenのBlocklist
class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    id = Column("id", String(255), primary_key=True, default=generate_uuid)
    jti = Column("jti", String(255), nullable=False)
    created_at = Column(
        "created_at", DATETIME, nullable=False, server_default=current_timestamp()
    )

    def __init__(self, jti):
        self.jti = jti
