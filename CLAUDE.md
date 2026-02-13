# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

---

## 项目概述

Rapport 是一个联系人长期记忆管理系统，能够将对话文本自动整理为四层联系人记忆模型（身份、状态、时间线、行动建议）。后端使用 FastAPI，前端使用 Vue 3 + uni-app，支持跨平台（H5 网页、微信小程序）。

---

## 架构

### 后端 (FastAPI + MySQL)

```
backend/app/
├── api/          # 路由处理器 (auth.py, contacts.py)
├── core/         # 配置、安全 (JWT、密码哈希)
├── models/       # SQLAlchemy ORM 模型 + Pydantic schemas
├── services/     # 业务逻辑 (contact_service.py, llm_service.py)
└── main.py       # FastAPI 应用入口
```

**关键模式：**
- `models/schemas.py` 中的 Pydantic schemas 定义所有 API 契约
- `database.py` 提供 `get_db()` 依赖用于会话注入
- `dependencies.py` 中的 `get_current_user` 用于需要认证的路由
- LLM 服务 (`llm_service.py`) 处理结构化提取，带重试逻辑

### 前端 (Vue 3 + uni-app)

```
frontend/src/
├── api/          # API 客户端，带请求封装
├── components/    # 可复用的 Vue 组件
├── pages/         # uni-app 页面（通过 pages.json 路由）
├── store/         # Pinia 状态管理，带持久化
├── types/         # TypeScript 类型定义
└── utils/         # 工具函数
```

**关键模式：**
- `pages.json` 定义路由和 tabBar（uni-app 约定）
- Pinia stores 使用 `persist: true` 进行 localStorage 同步
- API 客户端封装 `uni.request`，自动注入 token
- 组件通过 pages.json 中的 `easycom` 自动导入

---

## 开发命令

### 后端

```bash
cd backend

# 安装依赖（推荐使用 uv）
pip install uv && uv sync
# 或: pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑 .env: DATABASE_URL, LLM_API_KEY, SECRET_KEY

# 数据库迁移
alembic upgrade head                              # 应用迁移
alembic revision --autogenerate -m "描述"        # 创建新迁移
alembic downgrade -1                             # 回滚

# 运行开发服务器
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 配置环境
cp .env.example .env

# 开发模式
npm run dev:h5            # H5 网页 (http://localhost:5173)
npm run dev:mp-weixin      # 微信小程序

# 生产构建
npm run build:h5
npm run build:mp-weixin
```

### 快速启动（前后端）

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh && ./start.sh
```

---

## 四层记忆模型

核心业务逻辑将联系人数据组织为四层：

1. **Identity**（A 层）- 稳定画像：姓名、教育、职业概述、沟通偏好
2. **Status**（B 层）- 动态状态：当前工作、目标、资源需求/供给、情绪上下文
3. **Timeline**（C 层）- 只追加的互动历史：会谈记录，包含主题、事实、承诺、续聊钩子
4. **Action Playbook**（D 层）- 衍生建议：送礼偏好、续聊钩子、合作地图、关系健康分

**实现方式：**
- `Contact` ORM 模型存储 Identity + Status 字段
- `Meeting` ORM 模型存储 Timeline 记录
- `ActionPlaybook` ORM 模型存储 D 层建议
- `llm_service.py` 中的 LLM 提示词强制使用此 schema 进行提取

---

## API 端点

基础 URL: `/api/v1`

**认证：**
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录（返回 JWT）

**联系人：**
- `GET /contacts?search=关键词` - 联系人列表
- `POST /contacts` - 创建联系人
- `GET /contacts/{id}/timeline` - 获取完整联系人（含会谈 + 行动建议）
- `GET /contacts/{id}/export` - 导出为 Markdown
- `PUT /contacts/{id}` - 更新联系人
- `DELETE /contacts/{id}` - 删除联系人

**会谈：**
- `POST /meetings` - 从对话文本创建（LLM 处理）
- `POST /contacts/{id}/meetings` - 为联系人添加会谈记录

---

## 常见任务对应的文件

| 任务 | 文件 |
|------|--------|
| 添加 API 端点 | `backend/app/api/*.py`，添加路由，更新 schemas |
| 添加数据库字段 | `backend/app/models/models.py`，创建 Alembic 迁移 |
| 修改 LLM 提示词 | `backend/app/services/llm_service.py` |
| 添加前端页面 | 在 `frontend/src/pages/` 创建，更新 `pages.json` |
| 更新状态 | `frontend/src/store/*.ts` (Pinia) |
| API 变更 | `frontend/src/api/index.ts`，`frontend/src/types/index.ts` |

---

## LLM 集成

`LLMService` 类 (`backend/app/services/llm_service.py`) 处理对话文本处理：

- 使用 OpenAI 兼容 API（通过 `LLM_BASE_URL` 配置）
- 强制输出匹配四层模型的 JSON schema
- 实现重试逻辑（默认：2 次）
- System prompt 定义所有提取字段，使用中文标签

**通过 `.env` 配置：**
- `LLM_API_KEY` - API 密钥
- `LLM_BASE_URL` - API 端点（默认：OpenAI）
- `LLM_MODEL` - 模型名称（默认：gpt-4o）

---

## 前端路由

uni-app 使用 `pages.json` 进行路由（非 Vue Router）：

```json
{
  "pages": [
    { "path": "pages/index/index", ... },
    { "path": "pages/login/login", ... }
  ],
  "tabBar": {
    "list": [{ "pagePath": "pages/index/index", ... }]
  }
}
```

导航使用 `uni.navigateTo()` 跳转普通页面，`uni.switchTab()` 切换 tabBar 页面。

---

## 数据库结构

核心表：`users`、`contacts`、`meetings`、`action_playbooks`

主要关系：
- `contacts.user_id` → `users.id`
- `meetings.contact_id` → `contacts.id`
- `action_playbooks.contact_id` → `contacts.id` (一对一)

所有时间戳使用时区感知的 datetime。JSON 字段存储数组（topics、goals 等）。
