from flask import Blueprint, jsonify, g

from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

__author__ = 'lybin'
__date__ = '2018/12/5 19:57'

api = Redprint('user')


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    # 普通用户调用的接口
    # 通过token来验证才能访问
    # 先验证token是否合法，然后验证是否过期
    # 由于验证的请求很多，所以采用装饰器的方式验证
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    # 这种方式是最简单，且容易理解的返回方式
    # r = {
    #     'nickname': user.nickname,
    #     'email': user.email
    # }
    # return jsonify(r)
    # 换用高级一些的方式来返回
    return jsonify(user)


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    # 管理员才能调用的接口
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    # 用户主动注销账号
    # 考虑超权的问题，不能直接传递uid
    # 由于g是线程隔离的，所以用户的同步请求也不会发生数据错乱
    uid = g.user.uid
    with db.auto_commit():
        # 不能采用这种方式，因为一旦软删除了还可以查询到用户
        # user = User.query.get_or_404(uid)
        user = User.query.filter_by(id=uid).first_or_4o4()
        user.delete()
    return DeleteSuccess()


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    # 管理员删除账户
    with db.auto_commit():
        # 不能采用这种方式，因为一旦软删除了还可以查询到用户
        # user = User.query.get_or_404(uid)
        user = User.query.filter_by(id=uid).first_or_4o4()
        user.delete()
    return DeleteSuccess()



@api.route('', methods=['PUT'])
def update_user():
    return 'update lyb'
