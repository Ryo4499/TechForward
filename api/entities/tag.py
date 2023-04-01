from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from entities.article_tag import ArticleTag
from . import Base
from .utils import generate_uuid


# Tagのテーブル
class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    tagId = Column("id", String(255), primary_key=True, default=generate_uuid)
    tagName = Column("tag_name", String(255), nullable=False, index=True, unique=True)

    articles = relationship("Article", secondary=ArticleTag, back_populates="tags")

    def __init__(self, tagName, tagId=None):
        self.tagId = tagId
        self.tagName = tagName
