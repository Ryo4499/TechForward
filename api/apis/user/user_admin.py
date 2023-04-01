from traceback import format_exception_only
from flask import Response
from flask_restful import Resource
from jwt_token import admin_required
from sqlalchemy import desc
from ..utils.pagination import Pagination
from entities import Session
from entities.user import User
from schemas.user import UserSchema
from helper.message import (
    PAGE_VALUE_ERROR,
    USER_NOT_FOUND,
)
from helper.error import ErrorHandler
from helper.response import ResponseHandler


# 全ユーザを取得
class UsersAdminAPI(Resource):
    @admin_required
    def get(self) -> Response:
        """全ユーザーの取得

        Returns:
            Response: 正常系または異常系のレスポンス
        """
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))
        with Session() as session:
            users = (
                session.query(User)
                .order_by(desc(User.updatedAt), desc(User.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = session.query(User).count()
            session.commit()

            # ユーザ一覧が空リストなら
            if users == [] or count == 0:
                return ResponseHandler.res204({"message": USER_NOT_FOUND})

            return ResponseHandler.res200(
                UserSchema(
                    many=True,
                ).dump(users),
                count,
            )
