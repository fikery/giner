from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from werkzeug.exceptions import HTTPException

__author__ = 'lybin'
__date__ = '2018/12/5 21:26'

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: _register_user_by_email,

    }
    promise[form.type.data]()

    return Success()


def _register_user_by_email():
    '''处理email注册类型的客户端'''
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
