from app.libs.error_code import ServerError

__author__ = 'lybin'
__date__ = '2018/12/5 19:46'

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from datetime import date


class JSONEncoder(_JSONEncoder):
    '''重写json的默认default序列化'''

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            # 对于不能序列化的对象，单独处理
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    '''继承原Flask对象，重写default方法，使得对象可以被序列化'''
    json_encoder = JSONEncoder
