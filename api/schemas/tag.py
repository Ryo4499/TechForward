import re
from jsonschema.exceptions import ValidationError
from marshmallow.decorators import validates_schema
from sqlalchemy.orm import load_only
from marshmallow import post_load, EXCLUDE
from marshmallow.validate import Length, Regexp
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Tag
from models.setting import REGEX_PATTERN, Session
from marshmallow_sqlalchemy.schema import auto_field


class TagSchema(SQLAlchemyAutoSchema):

    tagId = auto_field()
    tagName = auto_field(
        validate=Length(min=1, max=30),
        required=True,
        error_messages={"required": "タグ名は必須項目です｡", "code": 400},
    )

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        p = re.compile(REGEX_PATTERN)
        if not p.fullmatch(data["tagName"]):
            raise ValidationError("全角文字､半角英数字で入力して下さい｡")

    class Meta:
        model = Tag
        include_fk = True
        include_relationship = True
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        strict = True
        sqla_session = Session

        @post_load
        def make_tag(self, data, **kwargs):
            return Tag(**data)
