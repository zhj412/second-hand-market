# 二手交易平台（Django 软件测试练手项目）

一个基于 **Python + Django** 开发的二手交易平台，包含用户、商品、购物车、订单、收藏、站内消息等完整业务功能，后台管理使用 [django-simpleui](https://github.com/newpanjing/simpleui) 美化主题。本项目定位为**软件测试练手项目**，可用于功能测试、接口测试、回归测试、兼容性测试等实践练习。

---

## 目录

- [技术栈](#技术栈)
- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [快速开始（部署步骤）](#快速开始部署步骤)
- [测试账号](#测试账号)
- [功能模块与测试说明](#功能模块与测试说明)
- [自动化测试](#自动化测试)
- [接口测试](#接口测试)
- [性能测试](#性能测试)
- [常用命令](#常用命令)
- [注意事项](#注意事项)

---

## 技术栈

| 类别 | 技术 |
| --- | --- |
| 后端框架 | Django 4.2 |
| 数据库 | MySQL（utf8mb4） |
| 前端 | HTML / CSS / JavaScript / Bootstrap（服务端模板渲染） |
| 后台主题 | django-simpleui |
| 数据库驱动 | mysqlclient |
| 图片处理 | Pillow |
| 环境变量 | python-dotenv |
| 运行环境 | Python 3.8～3.12（本项目开发环境为 3.11） |

## 功能特性

- **用户模块**：注册、登录、退出、个人中心
- **商品模块**：商品分类、商品发布、商品列表、商品详情
- **购物车模块**：加入购物车、查看购物车
- **订单模块**：下单购买、订单列表、订单详情
- **收藏模块**：收藏 / 取消收藏商品
- **消息模块**：站内消息收发
- **管理后台**：SimpleUI 主题，商品 / 订单 / 用户 / 分类 / 消息管理

## 项目结构

```
second_hand_market/
├── manage.py                 # Django 管理入口
├── requirements.txt          # Python 依赖清单
├── .env.example              # 环境变量模板（提交到仓库）
├── .env                      # 本地环境变量（已被 .gitignore 忽略）
├── .gitignore                # Git 忽略规则
├── second_hand_market.sql    # 数据库导出（含建表与初始数据）
├── 运行脚本.bat               # Windows 双击启动脚本
├── import_test_data.py       # 导入测试数据脚本
├── bind_goods_images.py      # 绑定商品图片脚本
├── second_hand_market/       # 项目配置（settings / urls / wsgi / asgi）
├── users/                    # 用户模块
├── goods/                    # 商品模块
├── cart/                     # 购物车模块
├── order/                    # 订单模块
├── favorite/                 # 收藏模块
├── message/                  # 消息模块
├── templates/                # 前端模板
├── static/                   # 静态资源（css / js / images）
└── media/                    # 用户上传文件（已被 .gitignore 忽略）
```

---

## 快速开始（部署步骤）

### 1. 环境要求

- Python 3.8～3.12（Django 4.2 兼容范围，**请勿使用 3.13 / 3.14**，推荐 3.11）
- MySQL 5.7 或 8.0
- 已安装 Git（用于克隆项目）

### 2. 克隆项目

```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> Windows 下若 `mysqlclient` 安装失败，可先安装对应版本的 `.whl` 轮子，或改用 `pip install pymysql`（需同步修改 `settings.py` 中的数据库 ENGINE）。

### 4. 配置环境变量（.env）

复制模板文件并填写你的数据库信息：

```bash
# Linux / macOS
cp .env.example .env

# Windows
copy .env.example .env
```

打开 `.env`，按实际情况修改：

```ini
DJANGO_SECRET_KEY=请填写你的SECRET_KEY        # 可用下方命令生成
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DB_NAME=second_hand_market                    # 数据库名
DB_USER=root                                  # 数据库用户名
DB_PASSWORD=你的数据库密码                      # 数据库密码
DB_HOST=127.0.0.1
DB_PORT=3306
```

生成随机 SECRET_KEY：

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. 创建数据库

在 MySQL 中执行（或使用 Navicat 等工具创建）：

```sql
CREATE DATABASE second_hand_market CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 初始化数据（二选一）

#### 方式 A：直接导入 SQL（推荐，含完整数据与 admin 账号）

```bash
# 命令行导入
mysql -u root -p second_hand_market < second_hand_market.sql

# 或使用 Navicat：新建 second_hand_market 库 → 右键「运行 SQL 文件」→ 选择 second_hand_market.sql
```

#### 方式 B：迁移建表 + 导入测试数据

```bash
python manage.py migrate              # 根据 migrations 建表
python manage.py createsuperuser      # 手动创建管理员账号
python import_test_data.py            # 导入测试用户、分类、商品等数据
```

### 7. 启动服务

```bash
python manage.py runserver 8080
```

或在 Windows 下**双击 `运行脚本.bat`** 直接启动。

### 8. 访问

| 入口 | 地址 |
| --- | --- |
| 前台首页 | http://127.0.0.1:8080/ |
| 管理后台 | http://127.0.0.1:8080/admin/ |

---

## 测试账号

| 账号 | 密码 | 说明 |
| --- | --- | --- |
| admin | admin123 | 管理员（由 SQL 导入；方式 B 需自行 `createsuperuser`） |
| user1 | 123456 | 普通用户（由 `import_test_data.py` 创建） |
| user2 | 123456 | 普通用户 |
| user3 ~ user5 | 123456 | 普通用户 |

---

## 功能模块与测试说明

| 模块 | 主要功能 | 建议测试点 |
| --- | --- | --- |
| **用户（users）** | 注册、登录、退出、个人中心 | 注册参数校验（用户名/密码一致性）、重复注册、登录成功/失败、会话保持、退出后会话失效、个人资料展示 |
| **商品（goods）** | 分类、发布、列表、详情 | 商品分类层级、发布表单校验（价格/描述）、列表分页与筛选、详情页字段展示、浏览量统计、未登录发布限制 |
| **购物车（cart）** | 加入购物车、查看 | 加入购物车、重复加入、数量累计、空购物车展示、未登录访问控制 |
| **订单（order）** | 下单、订单列表、详情 | 下单流程、买家/卖家视角、订单状态流转、订单详情字段、关联商品与用户 |
| **收藏（favorite）** | 收藏 / 取消收藏 | 收藏商品、重复收藏去重、取消收藏、收藏列表、未登录访问控制 |
| **消息（message）** | 站内消息收发 | 发送消息、已读/未读状态、收件箱/发件箱、消息内容展示 |
| **后台管理（admin + SimpleUI）** | 各模块增删改查 | 后台登录、菜单展示、商品/订单/用户/分类/消息的增删改查、权限控制 |

> 本项目已针对上述模块编写了完整的自动化测试用例（共 **85 个**），详见下方「自动化测试」章节。

---

## 自动化测试

项目内置 **85 个自动化测试用例**（功能测试 64 + 接口测试 21），当前代码覆盖率 **100%**。

### 运行测试

推荐使用 **pytest**（测试专用 SQLite 内存库，无需 MySQL、速度更快）：

```bash
# 先安装测试依赖
pip install -r requirements-dev.txt

# 运行全部测试并生成覆盖率报告
py -3.11 -m pytest

# 只运行某个模块 / 某个测试类
py -3.11 -m pytest goods
py -3.11 -m pytest users/tests.py::UserLoginViewTest
```

也可以使用 Django 自带的测试命令（默认连接 MySQL）：

```bash
py -3.11 manage.py test
```

### 代码覆盖率

当前代码覆盖率 **100%**（共 391 行语句）。运行 `pytest` 后：
- 终端会打印每个模块的覆盖率与未覆盖行；
- 打开 `htmlcov/index.html` 可查看可视化覆盖率报告。

### 持续集成（CI）

项目已配置 GitHub Actions（`.github/workflows/tests.yml`），每次 **push** 或 **Pull Request** 都会自动用 Python 3.11 运行全部测试，仓库的「Actions」标签可查看运行结果。

> 完整的测试报告见 [docs/测试报告.md](docs/测试报告.md)。

### 测试覆盖范围

| 模块 | 测试类 | 覆盖内容 |
| --- | --- | --- |
| 首页 | `HomeViewTest` | 页面可访问、只显示在售商品、展示顶级分类 |
| 用户 | `UserProfileModelTest` / `UserRegisterViewTest` / `UserLoginViewTest` / `UserLogoutViewTest` / `UserProfileViewTest` | 模型、注册（含重复注册/密码不一致）、登录（含错误密码）、退出、个人中心更新与登录保护 |
| 商品 | `CategoryModelTest` / `GoodsModelTest` / `GoodsListViewTest` / `GoodsPublishViewTest` / `GoodsDetailViewTest` | 分类自关联、商品模型、列表搜索/筛选/排序、发布必填校验、详情浏览量自增与 404 |
| 购物车 | `CartModelTest` / `CartListViewTest` | 唯一约束、默认数量、登录保护、只看自己的购物车 |
| 订单 | `OrderModelTest` / `OrderListViewTest` / `OrderDetailViewTest` | 模型、买家视角列表、他人订单返回 404 |
| 收藏 | `FavoriteModelTest` / `FavoriteListViewTest` | 唯一约束、登录保护、只看自己的收藏 |
| 消息 | `MessageModelTest` / `MessageListViewTest` | 默认已读状态、登录保护、只看收到的消息 |

> 测试覆盖了「模型单元测试」「视图功能测试」「登录鉴权」「404 / 302 跳转」「筛选与排序」等常见测试场景，可作为功能测试 / 回归测试的学习范例。

---

## 接口测试

项目使用 Django REST Framework 提供 RESTful 接口，采用 Token 认证。

### 接口列表

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/api/goods/` | 商品列表（支持 `q` 搜索、`category` 筛选） | 公开 |
| GET | `/api/goods/<id>/` | 商品详情 | 公开 |
| POST | `/api/goods/` | 发布商品 | 登录 |
| GET | `/api/categories/` | 分类列表 | 公开 |
| POST | `/api/register/` | 注册（返回 Token） | 公开 |
| POST | `/api/login/` | 登录（返回 Token） | 公开 |
| GET | `/api/orders/` | 我的订单 | 登录 |
| GET / POST / DELETE | `/api/favorites/` | 收藏 / 取消收藏 | 登录 |
| GET / POST | `/api/cart/` | 我的购物车 | 登录 |
| GET | `/api/messages/` | 我的消息 | 登录 |

接口测试共 **21 个用例**（见 `api/tests.py`），覆盖增删查、Token 鉴权（匿名 401）、数据隔离等场景。

## 性能测试

使用 [Locust](https://locust.io/) 对关键页面与接口进行并发压测，脚本见 `locustfile.py`。

```bash
# 1. 启动服务
py -3.11 manage.py runserver 8080
# 2. 压测（50 并发用户，持续 20 秒）
py -3.11 -m locust -f locustfile.py --headless -u 50 -r 10 -t 20s --host http://127.0.0.1:8080
```

参考结果（本地开发服务器，50 并发 / 20 秒）：

| 接口 | 请求数 | 平均响应 | 最大响应 | 失败率 |
| --- | --- | --- | --- | --- |
| `/` 首页 | 224 | 12 ms | 57 ms | 0% |
| `/goods/` 商品列表 | 118 | 11 ms | 55 ms | 0% |
| `/api/goods/` 商品接口 | 90 | 12 ms | 58 ms | 0% |
| `/user/login/` 登录页 | 37 | 3 ms | 14 ms | 0% |

总请求 469 次，**失败率 0%**，平均响应时间约 11 ms，吞吐量约 24 req/s。

---

## 常用命令

```bash
python manage.py runserver 8080     # 启动开发服务器
python manage.py check              # 检查项目配置
python manage.py makemigrations     # 生成迁移文件
python manage.py migrate            # 执行数据库迁移
python manage.py createsuperuser    # 创建超级管理员
python import_test_data.py          # 导入测试数据
python manage.py shell              # 进入 Django shell
```

---

## 注意事项

- **`.env` 包含数据库密码等敏感信息，已被 `.gitignore` 排除，请勿提交到仓库**；`.env.example` 为模板，可正常提交。
- `media/` 目录存放用户上传的图片，同样已被 `.gitignore` 排除，克隆后需自行上传商品图片（或使用 `bind_goods_images.py` 绑定本地图片）。
- 本项目默认 `DEBUG = True` 用于本地开发；**生产环境请关闭 DEBUG、修改 SECRET_KEY 并配置 ALLOWED_HOSTS**。
- 本项目仅用于软件测试学习与练手，请勿用于商业用途。
