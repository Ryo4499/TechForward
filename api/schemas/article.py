import re
from jsonschema.exceptions import ValidationError
from marshmallow.decorators import validates_schema
from .tag import TagSchema
from .user import UserSchema
from sqlalchemy.orm import load_only
from marshmallow import fields, post_load, EXCLUDE
from marshmallow.validate import Length, Regexp
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Article
from models.setting import Session
from marshmallow_sqlalchemy.schema import auto_field


class ArticleSchema(SQLAlchemyAutoSchema):

    userId = auto_field(load_only=True)
    articleId = auto_field()
    title = auto_field()
    content = auto_field()
    draft = fields.Boolean()
    isActivate = fields.Boolean()
    createdAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    updatedAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    user = fields.Nested(lambda: UserSchema(only=("userName",)), lazy="subquery")
    tags = fields.Pluck(TagSchema, "tagName", many=True, lazy="subquery")
    comments = auto_field(lazy="subquery")

    class Meta:
        model = Article
        include_fk = True
        include_relationships = True
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        strict = True
        sqla_session = Session

        @post_load
        def make_article(self, data, **kwargs):
            return Article(**data)


adminReqSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "pattern": "^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$",
            "minlength": 1,
            "maxlength": 50,
        },
        "content": {
            "type": "string",
            "minlength": 1,
            "maxlength": 5000,
        },
        "draft": {
            "type": "boolean",
        },
        "isActivate": {
            "type": "boolean",
            "nullable": True,
            "default": True,
        },
        "tags": {
            "type": "array",
            "null"
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 30,
            },
            "nullable": True,
            "default": None,
            "minItems": 1,
            "maxItems": 5,
        },
    },
    "required": ["title", "content", "draft", "isActivate"],
}

userReqSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "pattern": "^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$",
            "minLength": 1,
            "maxLength": 50,
        },
        "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000,
        },
        "draft": {"type": "boolean"},
        "tags": {
            "type": "array",
            "null"
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 30,
            },
            "default": None,
            "minItems": 1,
            "maxItems": 5,
            "uniqueItems": True,
        },
    },
    "required": ["title", "content", "draft"],
}
