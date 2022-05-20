import re
from jsonschema.exceptions import ValidationError
from marshmallow.decorators import validates_schema
from sqlalchemy.orm import load_only, noload
from api.models import User
from api.models.setting import USERNAME_PATTERN,PASSWORD_PATTERN, Session
from marshmallow import fields, post_load, EXCLUDE
from marshmallow.validate import And, Equal, Length, OneOf, Email, Regexp
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchema, auto_field


class UserSchema(SQLAlchemyAutoSchema):

    userId = auto_field()
    userName = auto_field(
        validate=Length(min=1, max=30),
        required=True,
        error_messages={"required": "ユーザ名は必須項目です｡", "code": 400},
    )
    email = fields.Email(
        validate=And(
            Length(min=8, max=128),
            Email(),
        ),
        required=True,
        error_messages={"required": "Emailは必須項目です｡", "code": 400},
    )
    password = auto_field(
        load_only=True,
        validate=And(Length(min=8, max=128), Regexp(PASSWORD_PATTERN)),
        required=True,
        error_messages={"required": "パスワードは必須項目です｡", "code": 400},
    )
    createdAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    updatedAt = fields.DateTime("%Y-%m-%d %H:%M:%S", dump_only=True)
    isActivate = fields.Boolean(
        required=True,
        error_messages={"error": "trueまたはfalseを指定して下さい｡", "code": 400},
    )
    role = fields.Str(
        validate=OneOf(["user", "admin"]),
        error_messages={"error": "userまたはadminを指定して下さい｡", "code": 400},
    )
    articles = auto_field(load_only=True, lazy="subquery")
    comments = auto_field(load_only=True, lazy="subquery")

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if "userName" in data:
            p = re.compile(USERNAME_PATTERN)
            if not p.fullmatch(data["userName"]):
                raise ValidationError("ユーザ名は全角文字､半角英数字で入力して下さい｡")

    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        strict = True
        sqla_session = Session

        @post_load
        def make_user(self, data, **kwargs):
            return User(**data)
