from api.apis.pagination import Pagination
from traceback import format_exception_only
from api.token import admin_required
from api.helper.error import ErrorHandler
from api.helper.response import ResponseHandler
from sqlalchemy import desc
from flask_restful import Resource
from api.models.setting import Session
from api.models.user import User
from api.schemas.user import UserSchema
from api.helper.message import (
    PAGE_VALUE_ERROR,
    USER_NOT_FOUND,
)


# 全ユーザを取得
class UsersAdminAPI(Resource):
    @admin_required
    def get(self):
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
