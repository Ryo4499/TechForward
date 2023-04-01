from sqlalchemy import Column, String, Boolean, DATETIME
from sqlalchemy.orm import relationship, backref, Mapped
from sqlalchemy.sql.functions import func
from werkzeug.security import generate_password_hash, check_password_hash
from . import Base
from .utils import generate_uuid


# Userのテーブル
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    userId = Column("id", String(255), primary_key=True, default=generate_uuid)
    userName = Column("user_name", String(255), index=True, unique=True, nullable=False)
    email = Column("email", String(512), nullable=False)
    password = Column("password", String(512), nullable=False)
    role = Column("role", String(255), nullable=False)
    isActivate = Column("is_activate", Boolean, nullable=False, default=True)
    createdAt = Column(
        "created_at", DATETIME, nullable=False, server_default=func.now()
    )
    updatedAt = Column(
        "updated_at",
        DATETIME,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    articles = relationship("Article", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    def __init__(
        self,
        userName=None,
        email=None,
        password=None,
        userId=None,
        role="user",
        isActivate=True,
    ):
        self.password = password
        self.userId = userId
        self.userName = userName
        self.email = email
        self.role = role
        self.isActivate = isActivate

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
