from enum import Enum

__author__ = 'lybin'
__date__ = '2018/12/5 21:27'


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201
