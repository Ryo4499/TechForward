from flask import request
from entities.article import Article


class Pagination:
    def __init__(self, page: int = 0, perpage: int = 10):
        """ページネーションクラス

        Args:
            page (int, optional): 現在のページ. Defaults to 0.
            perpage (int, optional): 取得する件数. Defaults to 10.
        """
        self.page = page
        self.perpage = perpage
        self.DEFAULT_PAGE = 0
        self.DEFAULT_PERPAGE = 10

    def check_pagination(self):
        """page,perpageが０未満の場合に0または10に修正する"""
        # queryからpageとperpageを抽出
        args = request.args
        if "page" in args:
            if int(args["page"], 10) <= 0:
                self.page = self.DEFAULT_PAGE
            else:
                self.page = int(args["page"]) - 1
        if "perpage" in args:
            if int(args["perpage"], 10) <= 0:
                self.perpage = self.DEFAULT_PERPAGE
            else:
                self.perpage = int(args["perpage"])

    def sliceList(self, target: list[Article]) -> list[Article]:
        """記事のリストをpage*perpageから(page*perpage)+perpage個取得する

        Args:
            target (list[Article]): 記事のリスト

        Returns:
            list[Article]: page*perpageから(page*perpage)+perpage個取得した記事のリスト
        """
        return target[
            self.page * self.perpage : (self.page * self.perpage) + self.perpage
        ]

    def getPage(self) -> int:
        """paginationの開始位置取得

        Returns:
            int: 開始位置
        """
        return self.page * self.perpage
