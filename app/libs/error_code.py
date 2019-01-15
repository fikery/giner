from app.libs.error import APIException

__author__ = 'lybin'
__date__ = '2018/12/7 21:26'


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    msg = 'delete success'
    error_code = 1  # 删除成功


class ServerError(APIException):
    code = 500
    msg = 'oh NO, there is something wrong with the Server!'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'not...found -.-'
    error_code = 1001


class AuthFailed(APIException):
    '''授权失败'''
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(APIException):
    '''禁止跨权限访问'''
    code = 403
    msg = 'forbidden, not in scope'
    error_code = 1004