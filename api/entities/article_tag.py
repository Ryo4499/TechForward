from sqlalchemy import Table, Column, ForeignKey
from . import Base

# ArticleとTagの中間テーブル
ArticleTag = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
