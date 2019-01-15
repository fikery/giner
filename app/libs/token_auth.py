from collections import namedtuple

from flask import current_app, g, request

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

__author__ = 'lybin'
__date__ = '2018/12/8 20:50'


from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer\
    as Serializer, BadSignature, SignatureExpired

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    # 通过http的basicauth可以传递账号密码
    # 格式为header中提交key:value
    # key=Authorization
    # value=basic base64(account:password)
    # 实际上这里把token当作账号来传递，密码不用填
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)

    uid = data.get('uid')
    ac_type = data.get('type')
    scope = data.get('scope')
    # 此处可以获取request访问的视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)