from datetime import datetime
from api.helper.response import ResponseHandler
from api.apis.pagination import Pagination
from api.models.article import Article
from api.models.comment import Comment
from api.token import auth_required, get_jwt
from api.models.user import User
from traceback import format_exception_only
from api.helper.error import ErrorHandler
from sqlalchemy import desc
from marshmallow.exceptions import ValidationError
from api.schemas.comment import CommentSchema
from flask import request
from flask_restful import Resource
from api.models.setting import Session
from api.helper.message import (
    COMMENT_NOT_FOUND,
    ARTICLE_NOT_FOUND,
    PAGE_VALUE_ERROR,
    USER_NOT_FOUND,
)


class CommentAPI(Resource):
    @auth_required
    def get(self, commentId):
        with Session() as session:
            try:
                comment = session.query(Comment).filter_by(commentId=commentId).first()
                session.commit()

                if (
                    comment is None
                    or comment.article.isActivate == False
                    or comment.article.draft == True
                ):
                    return ErrorHandler.error404(COMMENT_NOT_FOUND)

                return ResponseHandler.res200(CommentSchema().dump(comment))
            except Exception as e:
                return ErrorHandler.error400(format_exception_only(type(e), e))

    @auth_required
    def put(self, commentId):
        with Session() as session:
            try:
                data = CommentSchema(only=("content",),).load(
                    request.get_json(),
                    session=session,
                )
            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error400(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))

            comment = session.query(Comment).filter_by(commentId=commentId).first()

            if comment is None:
                session.rollback()
                return ErrorHandler.error404(COMMENT_NOT_FOUND)

            if (
                comment.user.userId == get_jwt()["userId"]
                or get_jwt()["role"] == "admin"
            ):
                comment.content = data.content
                comment.updatedAt = datetime.now()
                session.add(comment)
                session.commit()
                return ResponseHandler.res200(CommentSchema().dump(comment))
            else:
                session.rollback()
                return ErrorHandler.error403()

    @auth_required
    def delete(self, commentId):
        with Session() as session:

            comment = session.query(Comment).filter_by(commentId=commentId).first()

            # タグが存在しない場合
            if comment is None:
                session.rollback()
                return ErrorHandler.error404(COMMENT_NOT_FOUND)

            if (
                comment.user.userId == get_jwt()["userId"]
                or get_jwt()["role"] == "admin"
            ):
                session.delete(comment)
                session.commit()
                return ResponseHandler.res200({"message": "削除されました｡"})
            else:
                session.rollback()
                return ErrorHandler.error403()


class CommentPostAPI(Resource):
    @auth_required
    def post(self, articleId):
        with Session() as session:
            try:
                comment = CommentSchema().load(
                    request.get_json(),
                    session=session,
                )
            except ValidationError as e:
                session.rollback()
                return ErrorHandler.error422(e.messages)
            except Exception as e:
                session.rollback()
                return ErrorHandler.error400(format_exception_only(type(e), e))
            try:
                article = (
                    session.query(Article)
                    .filter(
                        Article.articleId == articleId,
                        Article.isActivate == True,
                        Article.draft == False,
                    )
                    .first()
                )

                if article is None:
                    session.rollback()
                    return ErrorHandler.error404(ARTICLE_NOT_FOUND)

                user = (
                    session.query(User)
                    .filter(User.userId == get_jwt()["userId"], User.isActivate == True)
                    .first()
                )

                if user is None:
                    session.rollback()
                    return ErrorHandler.error404(USER_NOT_FOUND)

                comment.article = article
                comment.user = user
                session.add(comment)
                session.commit()

                return ResponseHandler.res201(
                    CommentSchema(
                        only=(
                            "commentId",
                            "article",
                            "content",
                            "user",
                            "createdAt",
                            "updatedAt",
                        )
                    ).dump(comment)
                )
            except Exception as e:
                session.rollback()

                return ErrorHandler.error400(format_exception_only(type(e), e))


class MyCommentsAPI(Resource):
    @auth_required
    def get(self):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            comments = (
                session.query(Comment)
                .join(User, Comment.userId == User.userId)
                .join(Article, Comment.articleId == Article.articleId)
                .filter(
                    User.userId == get_jwt()["userId"],
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .order_by(desc(Comment.updatedAt), desc(Comment.createdAt))
                .offset(pagination.getPage())
                .limit(pagination.perpage)
                .all()
            )
            count = (
                session.query(Comment)
                .join(User, Comment.userId == User.userId)
                .join(Article, Comment.articleId == Article.articleId)
                .filter(
                    User.userId == get_jwt()["userId"],
                    Article.isActivate == True,
                    Article.draft == False,
                )
                .count()
            )
            session.commit()

            if comments == [] or count == 0:
                return ResponseHandler.res204(COMMENT_NOT_FOUND)

            return ResponseHandler.res200(
                CommentSchema(many=True).dump(comments), count
            )


class CommentsByArticleAPI(Resource):
    @auth_required
    def get(self, articleId):
        # ページネーションのバリデーション
        try:
            pagination = Pagination()
            pagination.check_pagination()
        except ValueError as e:
            return ErrorHandler.error400(PAGE_VALUE_ERROR)
        except Exception as e:
            return ErrorHandler.error400(format_exception_only(type(e), e))

        with Session() as session:
            try:
                comments = (
                    session.query(Comment)
                    .join(Article, Comment.articleId == Article.articleId)
                    .filter(
                        Article.articleId == articleId,
                        Article.isActivate == True,
                        Article.draft == False,
                    )
                    .order_by(desc(Comment.createdAt), desc(Comment.updatedAt))
                    .offset(pagination.getPage())
                    .limit(pagination.perpage)
                    .all()
                )
                count = (
                    session.query(Comment)
                    .join(Article)
                    .filter(
                        Article.articleId == articleId,
                        Article.isActivate == True,
                        Article.draft == False,
                    )
                    .count()
                )
                session.commit()

                if comments == [] or count == 0:
                    return ResponseHandler.res204(COMMENT_NOT_FOUND)

                return ResponseHandler.res200(
                    CommentSchema(many=True).dump(comments), count
                )
            except Exception as e:
                session.rollback()

                ErrorHandler.error400(format_exception_only(type(e), e))
