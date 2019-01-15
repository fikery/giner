from flask import Blueprint
from app.api.v1 import user, book, client, token

__author__ = 'lybin'
__date__ = '2018/12/5 19:56'


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    # 红图向蓝图注册
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)

    return bp_v1
