from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

__author__ = 'lybin'
__date__ = '2018/12/8 20:00'

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    # 先对各种提交参数进行验证
    form = ClientForm().validate_for_api()
    # 再对用户账号密码进行验证
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    # 包装身份信息
    identify = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # 生成令牌token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identify.get('uid'),
                                form.type.data,
                                identify.get('scope'),
                                expiration)
    d = {
        'token': token.decode('ascii')
    }
    return jsonify(d), 201


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    '''生成令牌'''
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps(
        {
            'uid': uid,
            'type': ac_type.value,
            'scope': scope
        }
    )