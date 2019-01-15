from flask import Blueprint

from app.libs.redprint import Redprint

__author__ = 'lybin'
__date__ = '2018/12/5 19:57'

api = Redprint('book')


@api.route('', methods=['GET'])
def get_book():
    return 'get book'


@api.route('', methods=['POST'])
def create_book():
    return 'create_book'
