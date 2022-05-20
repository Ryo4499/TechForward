from api.helper.response import ResponseHandler
from api.apis.pagination import Pagination
from api.models.comment import Comment
from api.token import admin_required
from api.models.user import User
from traceback import format_exception_only
from api.helper.error import ErrorHandler
from sqlalchemy import desc
from api.schemas.comment import CommentSchema
from api.models.article import Article
from flask_restful import Resource
from api.models.setting import Session
from api.helper.message import COMMENT_NOT_FOUND, PAGE_VALUE_ERROR, ARTICLE_NOT_FOUND


class CommentsAdminAPI(Resource):
    @admin_required
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
            try:
                comments = (
                    session.query(Comment)
                    .order_by(
                        desc(Comment.updatedAt),
                        desc(Comment.createdAt),
                    )
                    .offset(pagination.getPage())
                    .limit(pagination.perpage)
                    .all()
                )
                count = session.query(Comment).count()
                session.commit()

                if comments == [] or count == 0:
                    return ResponseHandler.res204({"message": ARTICLE_NOT_FOUND})
                return ResponseHandler.res200(
                    CommentSchema(many=True).dump(comments), count
                )
            except Exception as e:
                session.rollback()
                ErrorHandler.error400(format_exception_only(type(e), e))


class CommentsByUserAdminAPI(Resource):
    @admin_required
    def get(self, userName):
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
                    .join(User)
                    .filter(User.userName == userName)
                    .order_by(
                        desc(Comment.updatedAt),
                        desc(Comment.createdAt),
                    )
                    .offset(pagination.getPage())
                    .limit(pagination.perpage)
                    .all()
                )
                count = (
                    session.query(Comment)
                    .join(User)
                    .filter(User.userName == userName)
                    .count()
                )
                session.commit()

                if comments == [] or count == 0:
                    return ResponseHandler.res204({"message": ARTICLE_NOT_FOUND})
                return ResponseHandler.res200(
                    CommentSchema(many=True).dump(comments), count
                )
            except Exception as e:
                session.rollback()
                ErrorHandler.error400(format_exception_only(type(e), e))


class SearchCommentContentAdminAPI(Resource):
    @admin_required
    def get(self, content):
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
                    .filter(Comment.content.contains(content))
                    .order_by(
                        desc(Comment.updatedAt),
                        desc(Comment.createdAt),
                    )
                    .offset(pagination.getPage())
                    .limit(pagination.perpage)
                    .all()
                )
                count = (
                    session.query(Comment)
                    .filter(Comment.content.contains(content))
                    .count()
                )
                session.commit()

                if comments == [] or count == 0:
                    return ResponseHandler.res204({"message": COMMENT_NOT_FOUND})
                return ResponseHandler.res200(
                    CommentSchema(many=True).dump(comments), count
                )
            except Exception as e:
                session.rollback()
                ErrorHandler.error400(format_exception_only(type(e), e))


class CommentsByArticleAdminAPI(Resource):
    @admin_required
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
                    )
                    .order_by(
                        desc(Comment.updatedAt),
                        desc(Comment.createdAt),
                    )
                    .offset(pagination.getPage())
                    .limit(pagination.perpage)
                    .all()
                )
                count = (
                    session.query(Comment)
                    .join(Article)
                    .filter(
                        Article.articleId == articleId,
                    )
                    .count()
                )
                session.commit()

                if comments == [] or count == 0:
                    return ResponseHandler.res204({"message": COMMENT_NOT_FOUND})

                return ResponseHandler.res200(
                    CommentSchema(many=True).dump(comments), count
                )
            except Exception as e:
                session.rollback()
                ErrorHandler.error400(format_exception_only(type(e), e))
