from schemas.user import UserSchema
from sqlalchemy.orm import load_only
from marshmallow import fields, post_load, EXCLUDE
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Comment
from models.setting import Session
from marshmallow_sqlalchemy.schema import auto_field


class CommentSchema(SQLAlchemyAutoSchema):
    commentId = auto_field()
    articleId = auto_field(load_only=True)
    userId = auto_field(load_only=True)
    content = auto_field(
        validate=Length(min=1, max=1000),
        required=True,
        error_messages={"required": "内容は必須項目です｡", "code": 400},
    )
    createdAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    updatedAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    article = auto_field(lazy="subquery")
    user = fields.Nested(lambda: UserSchema(only=("userName",)), lazy="subquery")

    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        strict = True
        sqla_session = Session

        @post_load
        def make_comment(self, data, **kwargs):
            return Comment(**data)
