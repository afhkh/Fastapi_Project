# Kong-OA-Backend

Kong-OA 办公自动化（OA）系统的后端项目，基于 **FastAPI** 构建，提供用户登录认证（JWT）、权限控制（RBAC）、服务器性能监控等接口，配合前端 `Kong_OA_FRONT`（Vue3 + Element Plus）使用。

## 技术栈

| 分类 | 技术 |
| --- | --- |
| Web 框架 | FastAPI |
| ORM | Tortoise ORM |
| 数据库 | MySQL / MariaDB |
| 数据库迁移 | Aerich |
| 认证 | JWT（python-jose） |
| 密码加密 | Passlib（bcrypt_sha256） |
| 日志 | Loguru |
| 配置管理 | pydantic-settings + python-dotenv |
| 系统监控 | psutil |
| ASGI 服务器 | Uvicorn |

## 功能模块

- **认证与鉴权**：用户登录，签发 JWT token；对外提供认证接口。
- **系统管理（RBAC）**：用户相关接口、权限相关接口，为 RBAC 权限模型预留结构。
- **首页 / 监控**：提供服务器性能信息接口（操作系统、CPU、磁盘、内存、网卡流量）。
- **日志与异常**：基于中间件记录访问日志，全局异常统一处理。

## 目录结构

```
Kong-OA-Backend/
├── logs/                         # 日志文件（info / error，按天切割）
├── migrations/                   # 数据库迁移记录（aerich 自动生成）
├── script/                       # 脚本文件
├── src/                          # 核心代码
│   ├── apps/                     # 各个业务 app
│   │   ├── home/                 # 首页 app
│   │   │   ├── __init__.py       # 首页相关 APIRouter
│   │   │   ├── models.py         # 首页用到的表
│   │   │   ├── schemas.py        # pydantic 模型（序列化 / 校验）
│   │   │   └── views/
│   │   │       └── views.py      # 首页视图函数
│   │   └── system/               # 系统功能（RBAC 核心）
│   │       ├── __init__.py       # 权限相关 APIRouter
│   │       ├── models.py         # RBAC 相关表
│   │       ├── schemas.py        # pydantic 模型
│   │       └── views/
│   │           ├── user.py       # 用户相关视图函数
│   │           └── auth.py       # 权限相关视图函数
│   ├── libs/                     # 第三方集成封装（短信、OSS、MinIO 等）
│   ├── utils/                    # 项目公共功能
│   │   ├── common_logger.py      # logger 封装
│   │   ├── common_middleware.py  # 中间件封装（CORS、访问日志）
│   │   ├── common_response.py    # 统一响应对象封装
│   │   ├── common_exception.py   # 全局异常封装
│   │   └── common_db.py          # 数据库封装
│   ├── __init__.py               # 创建 FastAPI app，注册路由 / 中间件 / 异常 / ORM
│   └── settings.py               # 项目配置（数据库、跨域、JWT 等）
├── main.py                       # 程序入口
├── pyproject.toml                # aerich 配置
└── learn.md                      # 开发学习笔记
```

## 快速开始

### 环境要求

- Python 3.10+
- MySQL / MariaDB

### 安装依赖

建议使用虚拟环境（项目已含 `.venv`）：

```bash
pip install fastapi uvicorn tortoise-orm aerich pydantic-settings python-dotenv
pip install python-jose[cryptography] passlib[bcrypt] loguru psutil aiomysql
```

### 配置环境变量

在项目根目录创建 `.env` 文件，配置以下项（`src/settings.py` 中的 `APPConfigSettings` 会读取）：

```env
APP_HOST=127.0.0.1
APP_PORT=8080

DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=kong_oa
```

### 数据库迁移（aerich）

```bash
aerich init -t src.utils.common_db.DB_ORM_CONFIG
aerich init-db
aerich migrate
aerich upgrade
```

### 启动服务

```bash
python main.py
```

服务默认运行在 `http://127.0.0.1:8080`。

## 接口约定

### 响应格式

所有接口通过 `common_response.APIResponse` 统一返回：

```json
{
  "code": 100,
  "msg": "成功",
  "data": {}
}
```

`code == 100` 表示业务成功，前端据此判断（见前端 `src/http/index.js` 的响应拦截器）。

### 路由前缀

- 首页接口：`/api/v1/home`
- 系统接口：`/api/v1/system`

### 接口一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/system/user/login` | 用户登录，返回 username / avatar / token |
| GET | `/api/v1/home/main/info` | 获取服务器性能信息（OS / CPU / 磁盘 / 内存 / 网卡） |
| GET | `/api/v1/home/main/logger_demo` | 日志使用示例 |

### 登录示例

请求：

```http
POST /api/v1/system/user/login
Content-Type: application/json

{
  "username": "admin",
  "password": "1234"
}
```

响应：

```json
{
  "code": 100,
  "msg": "成功",
  "username": "admin",
  "avatar": "avatar/default.png",
  "token": "<jwt-token>"
}
```

## 关键实现说明

- **统一响应**（`common_response.py`）：基于 `JSONResponse` 封装，默认 `code=100`、`msg=成功`。
- **全局异常**（`common_exception.py`）：自定义 `AuthException`（1001）、`LoginException`（1002），并兜底处理 `Exception`（9999），返回统一 JSON。
- **中间件**（`common_middleware.py`）：配置 CORS，并记录每次访问的客户端 IP、请求方式、路径、请求头、响应时间，写入响应头 `X-Process-Time`。
- **日志**（`common_logger.py`）：Loguru 按级别分离文件，info 日志每天 00:00 切割、保留 3 天；error 日志 500MB 切割、保留 4 周。
- **密码**（`system/models.py`）：使用 passlib 的 `bcrypt_sha256`，`make_password` 生成密文，`check_password` 校验。
- **JWT**（`system/views/user.py`）：登录成功后用 `python-jose` 以 `HS256` 签发 token，过期时间由 `ACCESS_TOKEN_EXPIRE_MINUTES` 控制。

## 相关文档

- 开发过程中的学习笔记见 [learn.md](./learn.md)
- 配套前端项目：`Kong_OA_FRONT`