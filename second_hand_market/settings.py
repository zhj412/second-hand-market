"""
Django settings for second_hand_market project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# 读取项目根目录下的 .env 文件
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 敏感配置统一从环境变量读取，下面为本地默认值
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-only-change-me')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'goods',
    'cart',
    'order',
    'favorite',
    'message',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'second_hand_market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'second_hand_market.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'second_hand_market'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 未登录用户访问受保护页面时跳转的登录页
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'home'

# DRF 接口配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLEUI_HOME_TITLE = '二手交易平台管理后台'
SIMPLEUI_HOME_ICON = 'fa fa-shopping-bag'
SIMPLEUI_DEFAULT_THEME = 'blue.css'


# SimpleUI 配置
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['商品管理', '交易管理', '用户管理', '认证和授权'],
    'dynamic': False,
    'menus': [
        {
            'app': 'goods',
            'name': '商品管理',
            'icon': 'fas fa-box',
            'models': [
                {'name': '商品列表', 'icon': 'fa fa-list', 'url': '/admin/goods/goods/'},
                {'name': '商品分类', 'icon': 'fa fa-tags', 'url': '/admin/goods/category/'},
            ],
        },
        {
            'app': 'order',
            'name': '交易管理',
            'icon': 'fas fa-shopping-cart',
            'models': [
                {'name': '订单管理', 'icon': 'fa fa-receipt', 'url': '/admin/order/order/'},
                {'name': '购物车', 'icon': 'fa fa-shopping-basket', 'url': '/admin/cart/cart/'},
                {'name': '收藏商品', 'icon': 'fa fa-heart', 'url': '/admin/favorite/favorite/'},
            ],
        },
        {
            'app': 'users',
            'name': '用户管理',
            'icon': 'fas fa-users',
            'models': [
                {'name': '用户信息', 'icon': 'fa fa-user', 'url': '/admin/users/userprofile/'},
                {'name': '站内消息', 'icon': 'fa fa-envelope', 'url': '/admin/message/message/'},
            ],
        },
        {
            'app': 'auth',
            'name': '认证和授权',
            'icon': 'fas fa-shield-alt',
            'models': [
                {'name': '用户', 'icon': 'fa fa-user', 'url': '/admin/auth/user/'},
                {'name': '组', 'icon': 'fa fa-users-cog', 'url': '/admin/auth/group/'},
            ],
        },
    ],
}

SIMPLEUI_HOME_TITLE = '二手交易平台'
SIMPLEUI_HOME_ICON = 'fa fa-shopping-bag'
SIMPLEUI_DEFAULT_THEME = 'blue.css'
