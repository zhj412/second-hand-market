"""测试环境专用配置。

使用 SQLite 内存数据库替代 MySQL，避免测试依赖本地数据库服务，
让本地与 GitHub Actions CI 都能快速、稳定地运行测试。
"""
from .settings import *  # noqa: F401,F403

# 覆盖数据库配置为 SQLite 内存数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
