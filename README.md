# LostAndFound 校园失物招领平台

一套基于 Django + Bootstrap 的校园失物招领平台。支持发布寻物/招领、搜索筛选、评论、站内私信、未读消息提醒等功能，适合作为课程项目或内部工具快速落地。

- 主要技术：Django 5 · Python 3.12 · Bootstrap 5
- 运行环境：Windows / macOS / Linux
- 授权协议：MIT

---

## 功能特性 🌟

- 物品信息
  - 发布/编辑/浏览寻物与招领信息（支持图片上传）
  - 搜索（标题/描述/地点），类别筛选
  - 留言评论
- 私信系统 💬
  - “私信”会话列表（与我聊过的所有用户）
  - 导航栏红点提醒（存在未读消息时显示）
  - 会话行的红色数字显示未读条数
  - 进入会话自动将“对方发给我”的未读设为已读
  - 返回按钮跳转到“私信列表”，避免浏览器回填输入内容
- 用户系统
  - 注册/登录/退出、个人资料、个人中心
- 界面与体验
  - 自适应布局，简洁主题
  - 首页英雄区、最新发布模块
  - 统一消息提示与表单校验

---

## 快速开始 🧰

### 前置条件

- Python 3.12+
- Git
- 推荐浏览器：Chrome

### 克隆与运行

```bash
# 1) 克隆仓库
git clone https://github.com/sincos1314/LostAndFound
cd LostAndFound

# 2) 创建并激活虚拟环境
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
# python -m venv venv
# source venv/bin/activate

# 3) 安装依赖
pip install -r requirements.txt

# 4) 初始化数据库
python manage.py migrate

# 5) 创建管理员账户
python manage.py createsuperuser

# 6) 启动开发服务器
python manage.py runserver
# 访问 http://127.0.0.1:8000/

# 7) 进入管理后台
# 访问 http://127.0.0.1:8000/admmin
```

---

## 项目结构 📁

```
LostAndFound/
├─ accounts/                       # 用户模块
│  └─ templates/accounts/
├─ items/                          # 物品模块
│  └─ templates/items/
├─ messaging/                      # 私信模块
│  ├─ templates/messaging/
│  └─ context_processors.py        # 导航栏未读总数
├─ lostandfound/                   # 项目配置
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ templates/                      # 公共模板
│  ├─ base.html
│  └─ home.html
├─ static/                         # 静态资源
│  ├─ css/style.css
│  ├─ js/main.js
│  └─ img/hero.svg (可选)
├─ media/                          # 用户上传（开发环境）
├─ manage.py
├─ requirements.txt
└─ README.md
```

---

## 配置说明 🔧

### 静态与媒体

- 开发环境（DEBUG=True）下 Django 自动服务 STATIC_URL 与 MEDIA_URL
- 生产环境需要收集静态资源：
  ```bash
  python manage.py collectstatic
  ```
- media/ 存放用户内容，不应提交到 Git（.gitignore 已忽略）

### 环境变量（可选，推荐）

使用 django-environ 管理敏感配置：

```bash
pip install django-environ
```

在 settings.py 中：

```python
import environ, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='dev-secret-key')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
```

创建 .env（勿提交到仓库）：

```
SECRET_KEY=请替换为安全随机串
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 私信与未读逻辑说明 💡

- 导航栏“私信”显示红点：表示存在未读消息（对方发给我的且未读）
- 私信列表每个会话右侧显示未读条数
- 进入会话页面时，自动将当前会话中“对方→我”的未读消息标记为已读
- 点击聊天页“返回”跳转到“私信列表”，该会话数字清零，其他会话不受影响

---

## 常见问题与排错 🐛

- 静态资源 404（如 hero.svg）
  - 原因：static/img/hero.svg 文件不存在
  - 解决：放置同名图片到 static/img/，或在 home.html 移除该图片引用
- 模板语法错误（TemplateSyntaxError）
  - 不要在 `{{ }}` 中写 Python 的 `and/or` 表达式
  - 使用模板标签：
    ```html
    bg-{% if condition %}a{% else %}b{% endif %}
    ```
- 数据迁移异常
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- 登录后“私信”不显示红点
  - 确认 settings.py 的 TEMPLATES → context_processors 中已加入：
    ```
    'messaging.context_processors.unread_totals',
    ```
  - 确保用户已登录且确有未读消息（对方发给我）

---

## 贡献指南 🤝

欢迎提交 Issue 或 Pull Request！

1. Fork 本仓库
2. 创建分支：`git checkout -b feat/your-feature`
3. 提交代码：`git commit -m "feat: your feature"`
4. 推送并发起 PR：`git push origin feat/your-feature`

---

## 许可证 📄

本项目基于 MIT License 发布。你可以自由地使用、修改和分发，但请保留版权与许可声明。

---

## 致谢 🙏

- Django 与其社区
- Bootstrap 团队
- 所有提出反馈和改进建议的使用者与贡献者