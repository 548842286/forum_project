#!/usr/bin/env python3
"""
社区论坛 - 启动脚本
"""

from app import create_app
from app.extensions import db
from app.models import User, Board

app = create_app()


def init_db():
    """初始化数据库和默认数据"""
    with app.app_context():
        db.create_all()

        # 创建默认板块
        default_boards = [
            {'name': '技术讨论', 'description': '编程、开发、技术的相关讨论'},
            {'name': '生活分享', 'description': '日常生活分享与交流'},
            {'name': '问答求助', 'description': '问题提问与寻求帮助'},
            {'name': '资源共享', 'description': '分享有价值的资源'},
        ]

        for board_data in default_boards:
            existing = Board.query.filter_by(name=board_data['name']).first()
            if not existing:
                board = Board(**board_data)
                db.session.add(board)

        db.session.commit()

        # 创建默认超级管理员
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='superadmin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('[初始化] 超级管理员已创建: admin / admin123')


def main():
    print('=' * 50)
    print('社区论坛系统启动')
    print('=' * 50)

    # 初始化数据库
    init_db()

    # 启动服务器
    print('[提示] 默认管理员账号: admin / admin123')
    print('[提示] 首次使用后请及时修改默认密码!')
    print('=' * 50)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
