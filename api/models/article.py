import re
from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy import Column, ForeignKey, String, Boolean, DATETIME, text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as Mediumtext
from sqlalchemy.orm import *
from sqlalchemy.sql.functions import current_timestamp, func
from models.article_tag import ArticleTag
from models.setting import Base, generate_uuid


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    articleId = Column("id", String(255), primary_key=True, default=generate_uuid)
    userId = Column(
        "user_id",
        String(255),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    title = Column("title", String(255), index=True, nullable=False)
    content = Column("content", Mediumtext, nullable=False)
    draft = Column("draft", Boolean, nullable=False)
    isActivate = Column("is_activate", Boolean, nullable=False, default=True)
    createdAt = Column(
        "created_at",
        DATETIME,
        nullable=False,
        server_default=func.now(),
    )
    updatedAt = Column(
        "updated_at",
        DATETIME,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = auto_field()
    comments = relationship("Comment", backref="article")
    tags = relationship(
        "Tag",
        secondary=ArticleTag,
        back_populates="articles",
    )

    def __init__(self, title, content, draft, articleId=None, isActivate=True):
        self.articleId = articleId
        self.title = title
        self.content = content
        self.draft = draft
        self.isActivate = isActivate
