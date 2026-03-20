# 社区论坛系统

一个基于 Flask 的轻量级论坛系统，支持用户发帖、评论和管理功能。

## 功能特性

- **用户系统**: 注册、登录、个人资料管理
- **帖子系统**: 发帖、编辑、删除、评论
- **板块管理**: 多板块分类、置顶帖子
- **管理员后台**: 帖子管理、用户管理、板块管理
- **超级管理员**: 权限管理、用户角色分配

## 技术栈

- 后端: Flask 3.0
- 数据库: SQLite (可通过配置切换其他数据库)
- 前端: Bootstrap 5 + Jinja2
- 认证: Flask-Login + Flask-WTF

## 安装和运行

### 1. 安装依赖

```bash
cd forum_project
pip install -r requirements.txt
```

### 2. 运行程序

```bash
python run.py
```

### 3. 访问系统

打开浏览器访问: http://localhost:5000

## 默认账号

- 超级管理员: `admin` / `admin123`
- 首次登录后请及时修改密码！

## 目录结构

```
forum_project/
├── app/
│   ├── __init__.py          # Flask应用工厂
│   ├── config.py            # 配置文件
│   ├── extensions.py        # 扩展初始化
│   ├── models/              # 数据模型
│   │   ├── user.py
│   │   ├── board.py
│   │   └── post.py
│   ├── views/               # 视图/路由
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── admin.py
│   │   └── superadmin.py
│   ├── forms/               # 表单定义
│   └── templates/           # Jinja2模板
├── static/                   # 静态资源
├── requirements.txt         # 依赖
└── run.py                   # 启动脚本
```

## 页面说明

### 主页 (/)
- 浏览所有帖子
- 按板块筛选
- 分页显示

### 用户相关
- `/auth/register` - 用户注册
- `/auth/login` - 用户登录
- `/auth/profile` - 个人资料

### 帖子相关
- `/post/create` - 发布帖子
- `/post/detail/<id>` - 帖子详情
- `/post/edit/<id>` - 编辑帖子

### 管理员后台
- `/admin/` - 管理面板
- `/admin/posts` - 帖子管理
- `/admin/users` - 用户管理
- `/admin/boards` - 板块管理

### 超级管理员后台
- `/superadmin/` - 超级管理面板
- `/superadmin/users` - 用户权限管理
