from traceback import format_exception_only
from schemas.tag import TagSchema
from helper.error import ErrorHandler
from helper.response import ResponseHandler
from flask import request
from marshmallow.exceptions import ValidationError
from flask_restful import Resource
from models.setting import Session
from models.tag import Tag
from jwt_token import admin_required
from helper.message import TAG_ALREADY_REGISTED, TAG_NOT_FOUND


class TagAdminAPI(Resource):
    @admin_required
    def put(self, tagId):
        with Session() as session:
            try:
                data = TagSchema(only=("tagName",),).load(
                    request.get_json(),
                    session=session,
                )
                tag = session.query(Tag).filter_by(tagId=tagId).first()
            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            # タグが存在しない場合
            if tag is None:
                session.rollback()
                return ErrorHandler.error400(TAG_NOT_FOUND)

            # 同じ名前で既に登録されているタグが存在しないなら
            already = (
                session.query(Tag)
                .filter(Tag.tagName == data.tagName, Tag.tagId != tag.tagId)
                .first()
            )

            if already is None:
                tag.tagName = data.tagName
                session.commit()
                return ResponseHandler.res200(TagSchema().dump(tag))

            session.rollback()
            return ErrorHandler.error400(TAG_ALREADY_REGISTED)

    @admin_required
    def delete(self, tagId):
        with Session() as session:
            tag = session.query(Tag).filter_by(tagId=tagId).first()

            # タグが存在しない場合
            if tag is None:
                session.rollback()
                return ErrorHandler.error404(TAG_NOT_FOUND)

            session.delete(tag)
            session.commit()

            return ResponseHandler.res200({"message": "削除されました｡"})
