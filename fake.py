__author__ = 'lybin'
__date__ = '2018/12/9 00:46'

'''离线脚本，可以超级超级管理员，或者模拟一些数据'''

from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建超级管理员
        user = User()
        user.nickname = 'admin'
        user.password = 'admin123'
        user.email = 'admin@qq.com'
        user.auth = 2
        db.session.add(user)