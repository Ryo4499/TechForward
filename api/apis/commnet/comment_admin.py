from flask import Response
from flask_restful import Resource
from jwt_token import admin_required
from traceback import format_exception_only
from sqlalchemy import desc
from schemas.comment import CommentSchema
from ..utils.pagination import Pagination
from entities.comment import Comment
from entities import Session
from entities.article import Article
from entities.user import User
from helper.error import ErrorHandler
from helper.message import COMMENT_NOT_FOUND, PAGE_VALUE_ERROR, ARTICLE_NOT_FOUND
from helper.response import ResponseHandler


class CommentsAdminAPI(Resource):
    @admin_required
    def get(self) -> Response:
        """コメントの全件取得

        Returns:
            Response: 正常系または異常系のレスポンス
        """
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
    def get(self, userName: str) -> Response:
        """ユーザごとのコメント全件取得

        Args:
            userName (str): ユーザ名

        Returns:
            Response: 正常系または異常系のレスポンス
        """
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
    def get(self, content: str) -> Response:
        """内容ごとのコメント全件取得

        Args:
            content (str): 検索する内容

        Returns:
            Response: 正常系または異常系のレスポンス
        """
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
    def get(self, articleId: str) -> Response:
        """記事ごとのコメント全件取得

        Args:
            articleId (str): 記事ID

        Returns:
            Response: 正常系または異常系のレスポンス
        """
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
