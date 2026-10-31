# Kong OA 后端

Kong OA 办公自动化系统的后端，使用 FastAPI、Tortoise ORM 和 MySQL，配合 Vue 前端提供登录、系统管理、菜单权限和请假管理接口。

## 技术栈

- FastAPI、Uvicorn、Pydantic
- Tortoise ORM、MySQL、Aerich 数据库迁移
- python-jose（JWT）、Passlib（密码哈希）
- Loguru、psutil、pydantic-settings、python-dotenv

## 功能模块

- **用户与权限**：用户登录、JWT 认证、角色及菜单权限、用户管理。
- **系统管理**：部门、岗位、角色和菜单的查询与维护。
- **办公管理**：请假申请、查询、修改、删除和审批。
- **首页**：服务器性能信息及日志示例。

## 环境准备

需要 Python 3.10 或更高版本，以及可连接的 MySQL 或 MariaDB。项目没有完整锁定依赖版本的文件，建议使用独立虚拟环境。

在项目根目录创建并激活虚拟环境（Windows PowerShell）：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装项目使用的依赖：

```powershell
python -m pip install fastapi uvicorn tortoise-orm aerich pydantic-settings python-dotenv
python -m pip install "python-jose[cryptography]" "passlib[bcrypt]" loguru psutil aiomysql
```

## 配置

在项目根目录创建 `.env`，根据本机环境填写，下面的密码和密钥仅是占位示例：

```dotenv
APP_HOST=127.0.0.1
APP_PORT=8080

DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=kong_oa

SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

配置由 `src/settings.py` 读取；数据库连接及模型注册位于 `src/utils/common_db.py`。先创建对应的数据库，并确保数据库用户有必要的访问权限。请勿提交真实密码或密钥。

## 数据库迁移

项目已经在 `pyproject.toml` 配置 Aerich，迁移文件位于 `migrations/`。运行命令前请确认 `.env` 指向预期数据库。

已有迁移记录的项目，在修改模型后通常执行：

```powershell
aerich migrate
aerich upgrade
```

`migrate` 生成迁移文件，`upgrade` 将待执行的迁移应用到数据库。初始化全新的 Aerich 项目时才使用 `aerich init` 和 `aerich init-db`；不要在已有业务数据库上随意重新初始化。应用迁移前请检查生成的变更并备份数据。

## 启动服务

确保数据库已启动、配置正确，且项目根目录存在 `media/` 和 `logs/` 目录：

```powershell
python main.py
```

程序使用 `.env` 中的 `APP_HOST` 和 `APP_PORT`。使用上面的示例配置时：

- API 地址：`http://127.0.0.1:8080`
- Swagger 文档：`http://127.0.0.1:8080/docs`
- ReDoc 文档：`http://127.0.0.1:8080/redoc`

前端默认请求 `http://127.0.0.1:8080/api/v1/`；更改后端地址或端口时，请同步检查前端配置和后端 CORS 配置。

## 接口概览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/v1/system/user/login` | 登录并获取 token |
| GET | `/api/v1/system/auth/auth` | 获取当前用户的菜单和按钮权限 |
| GET / POST / DELETE | `/api/v1/system/user/users` | 用户列表、新增、删除 |
| GET / PUT | `/api/v1/system/user/users/{user_id}` | 用户详情、修改 |
| GET / POST / DELETE | `/api/v1/system/role/roles` | 角色列表、新增、删除 |
| GET / POST / DELETE | `/api/v1/system/dept/depts` | 部门列表、新增、删除 |
| GET / POST / DELETE | `/api/v1/system/job/jobs` | 岗位列表、新增、删除 |
| GET / POST / DELETE | `/api/v1/system/menu/menus` | 菜单列表、新增、删除 |
| GET | `/api/v1/system/dept/tree/depts` | 部门树 |
| GET | `/api/v1/system/menu/tree/menus` | 菜单树 |
| GET / POST / DELETE | `/api/v1/oa/oa/leave` | 请假列表、新增、删除 |
| GET / PUT | `/api/v1/oa/oa/leave/{leave_id}` | 请假详情、修改 |
| GET | `/api/v1/oa/oa/leave/status/{leave_id}/{status_type}` | 审批请假 |
| GET | `/api/v1/home/main/info` | 服务器性能信息 |

请假列表参数 `q=1` 查询当前用户的记录，其他值查询全部记录。完整参数及响应以 `/docs` 和当前代码为准。

## 认证与响应

登录成功后，受认证保护的接口使用请求头：

```http
Authorization: Bearer <token>
```

普通响应由 `APIResponse` 提供，默认包含 `code` 和 `msg`；具体数据根据接口放在 `result`、`results` 或其他字段。例如：

```json
{
  "code": 100,
  "msg": "成功",
  "results": []
}
```

分页响应还包括 `total`、`page`、`page_size` 和 `has_next`。前端根据业务码 `100` 判断成功。

权限接口根据超级用户状态或关联角色返回菜单和按钮编码。前端对按钮的显示控制不能代替后端接口的权限校验；修改权限逻辑时应同时检查服务端访问控制。

## 测试数据

- `script/seed_demo_data.py`：添加带测试标记的数据；新建的测试账号及默认密码请查看脚本内容。脚本遇到同名的非测试记录会停止。
- `script/rebuild_demo_data.py`：备份数据库后重建部门、岗位、菜单和请假测试数据，保留已有账号及密码。**该脚本会删除并重建业务数据及部分关联关系**，仅应在确认目标是可重置的测试数据库后运行。

重建脚本的 JSON 备份位于 `backups/`，可能包含密码哈希等敏感信息，应妥善保管，避免提交或公开。

## 项目结构

```text
├── main.py                    # 应用入口
├── pyproject.toml             # Aerich 配置
├── migrations/                # 数据库迁移文件
├── script/                    # 数据脚本和学习示例
├── src/
│   ├── apps/
│   │   ├── home/              # 首页和服务器信息
│   │   ├── system/            # 用户、角色、菜单、部门、岗位
│   │   └── oa/                # 请假业务
│   ├── utils/                 # 数据库、响应、异常、日志、中间件
│   ├── settings.py            # 环境配置
│   └── __init__.py            # 应用创建与注册
├── media/                     # 媒体文件，通过 /media 访问
└── learn.md                   # 开发学习笔记
```

## 常见问题

- **连接数据库失败**：检查 MySQL 是否启动、`.env` 中的地址和凭据，以及目标数据库是否存在。
- **前端请求失败**：核对后端端口、前端基础地址、CORS 设置，并查看后端终端中的完整报错。
- **模型更改后缺少表或字段**：检查 Aerich 配置和迁移状态，确认迁移是否已应用到当前数据库。
- **登录后菜单或按钮缺失**：检查用户的超级管理员状态、角色与菜单关联，以及 `/api/v1/system/auth/auth` 的返回值。

配套前端项目为 `Kong_OA_FRONT`；更多开发记录见 [learn.md](./learn.md)。
