from app.libs.error_code import NotFound

__author__ = 'lybin'
__date__ = '2018/12/5 21:49'

from contextlib import contextmanager

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    '''派生出新的sql处理类，成为自带异常处理上下文的类'''

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    '''重写filter_by方法，默认增加查询添加status=1，这是对数据库进行软删除的状态标记'''

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super().filter_by(**kwargs)

    def get_or_404(self, ident):
        '''重写getor404方法，抛出自定义的API异常'''
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        '''重写first抛出API异常'''
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    '''作为一个表的基类，但是不创建这样的一个表,因此设置为一个抽象基类'''
    __abstract__ = True
    status = Column(SmallInteger, default=1)
    createTime = Column(Integer)

    def __init__(self):
        self.createTime = int(datetime.now().timestamp())

    def __getitem__(self, item):
        '''序列化时使用的'''
        return getattr(self, item)

    def setAttrs(self, attrsDict):
        '''动态为对象按属性赋值'''
        for k, v in attrsDict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    @property
    def createDateTime(self):
        '''将存储的时间戳转换为标准时间字符串格式'''
        if self.createTime:
            return datetime.fromtimestamp(self.createTime)
        else:
            return None

    def delete(self):
        self.status = 0
