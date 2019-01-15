from flask import request, json

__author__ = 'lybin'
__date__ = '2018/12/7 21:41'

from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    # 默认错误码
    code = 500
    # 默认错误信息
    msg = 'oh NO, there is something wrong with the Server!'
    # 自定义错误码
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super().__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_to_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_to_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
