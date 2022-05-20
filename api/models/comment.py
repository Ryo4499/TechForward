from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy import Column, ForeignKey, String, DATETIME, text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as Mediumtext
from sqlalchemy.orm import *
from sqlalchemy.sql.functions import current_timestamp, func
from api.models.setting import Base, generate_uuid


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    commentId = Column(
        "comment_id", String(255), primary_key=True, default=generate_uuid
    )
    articleId = Column(
        "article_id",
        String(255),
        ForeignKey("articles.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    userId = Column(
        "user_id",
        String(255),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    content = Column("content", Mediumtext, index=True, nullable=False)
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
    user = auto_field()
    article = auto_field()

    def __init__(self, content, commentId=None):
        self.commentId = commentId
        self.content = content
