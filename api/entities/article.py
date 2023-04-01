from sqlalchemy import Column, ForeignKey, String, Boolean, DATETIME
from sqlalchemy.dialects.mysql import MEDIUMTEXT as Mediumtext
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from entities.article_tag import ArticleTag
from . import Base
from .utils import generate_uuid


# Articleのテーブル
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

    user = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
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
