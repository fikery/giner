__author__ = 'lybin'
__date__ = '2018/12/9 11:22'


class Scope:
    '''权限基类'''
    allow_api = []  # 视图函数层面的权限控制
    allow_module = []  # 红图层面的权限控制
    forbidden = []  # 禁止访问当视图函数

    def __add__(self, other):
        self.allow_api.extend(other.allow_api)
        self.allow_api = list(set(self.allow_api))

        self.allow_module.extend(other.allow_module)
        self.allow_modulec = list(set(self.allow_module))

        self.forbidden.extend(other.forbidden)
        self.forbidden = list(set(self.forbidden))
        return self


class UserScope(Scope):
    '''普通用户的视图函数权限'''
    # allow_api = ['v1.user+get_user',
    #              'v1.user+delete_user']

    # 当模块中有大量视图函数可以被普通用户访问，较少被管理员访问
    # 可以采用禁止方式实现
    forbidden = ['v1.user+super_get_user',
                 'v1.user+super_delete_user']

    def __init__(self):
        self + AdminScope()


class AdminScope(Scope):
    '''管理员的视图函数权限，在低级权限的基础上，增加高级权限'''
    # allow_api = ['v1.user+super_get_user',
    #              'v1.user+super_delete_user']
    allow_module = ['v1.user']

    # def __init__(self):
    #
    #     self + UserScope()


class SuperScope(Scope):
    '''超级管理员权限'''
    pass
    # allow_api = ['v1.super_get_user']
    #
    # def __init__(self):
    #     self + AdminScope() + UserScope()


def is_in_scope(scope, endpoint):
    # 此时传入的scope是一个字符串，可能是'UserScope'
    # globals函数可以将当前模块的所有对象映射成一个字典
    # 通过字典取键的方式，得到scope的实例对象，进而调用属性
    # 当前是v1.view_func，蓝图+视图函数方式
    # 可以改为v1.user.view_func，蓝图+模块+视图函数方式
    # 也就是v1+redpoint+view_func,蓝图+红图+视图函数
    scope = globals().get(scope)()
    red_name = endpoint.split('+')[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
