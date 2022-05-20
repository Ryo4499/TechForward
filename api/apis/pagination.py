from flask import request


class Pagination:
    def __init__(self, page=0, perpage=10):
        self.page = page
        self.perpage = perpage

    def check_pagination(self):
        # queryからpageとperpageを抽出
        try:
            args = request.args
            if "page" in args:
                if int(args["page"], 10) <= 0:
                    self.page = 0
                else:
                    self.page = int(args["page"]) - 1
            if "perpage" in args:
                if int(args["perpage"], 10) <= 0:
                    self.perpage = 10
                else:
                    self.perpage = int(args["perpage"])
            pass
        except Exception as e:
            raise e

    def sliceList(self, target):
        if self.page is None or self.perpage is None:
            return target[0:10]
        else:
            return target[
                self.page * self.perpage : (self.page * self.perpage) + self.perpage
            ]

    # paginationの開始位置取得
    def getPage(self):
        return self.page * self.perpage
