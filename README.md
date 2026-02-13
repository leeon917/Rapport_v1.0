# Rapport - 联系人长期记忆管理系统

把一段对话文本自动整理成"联系人长期记忆"，方便下次快速接话与维护关系。

## 功能特性

- **对话文本分析**：粘贴对话内容，自动提取结构化信息
- **四层记忆模型**：
  - Identity（身份与稳定画像）
  - Status（当前状态与资源位）
  - Timeline（互动历史，递增追加）
  - Action Playbook（行动建议：送礼/续聊/合作/关系温度）
- **联系人管理**：搜索、查看详情
- **Markdown导出**：导出完整的联系人记忆
- **多端支持**：H5网页、微信小程序

## 技术栈

### 后端
- FastAPI - Web框架
- MySQL - 数据库
- Alembic - 数据库迁移
- OpenAI SDK - LLM集成

### 前端 (uni-app + Vue 3)
- Vue 3 - UI框架
- TypeScript - 类型安全
- uni-app - 跨平台框架
- Pinia - 状态管理
- Vite - 构建工具

## 项目结构

```
Rapport_v1.0/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/        # 业务服务
│   │   └── main.py         # 应用入口
│   ├── alembic/            # 数据库迁移
│   ├── pyproject.toml      # Python依赖
│   └── requirements.txt
│
├── frontend/               # uni-app 前端项目
│   ├── src/
│   │   ├── api/            # API服务
│   │   ├── components/     # Vue组件
│   │   ├── pages/          # 页面
│   │   ├── store/          # Pinia状态管理
│   │   ├── types/          # TypeScript类型
│   │   ├── utils/          # 工具函数
│   │   ├── App.vue         # 应用入口
│   │   ├── main.ts         # 主入口
│   │   ├── pages.json      # 页面配置
│   │   └── manifest.json   # 应用配置
│   ├── index.html
│   └── package.json
│
├── README.md
├── start.bat               # Windows启动脚本
└── start.sh                # Linux/Mac启动脚本
```

## 快速开始

### 1. 数据库准备

创建MySQL数据库：

```sql
CREATE DATABASE rapport CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 后端启动

```bash
cd backend

# 安装依赖（使用uv）
pip install uv
uv sync

# 或使用pip
pip install -r requirements.txt

# 复制环境变量
cp .env.example .env

# 编辑.env，配置数据库和LLM API密钥

# 运行数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

后端服务将在 http://localhost:8000 启动

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 复制环境变量
cp .env.example .env

# H5开发模式
npm run dev:h5

# 微信小程序开发模式
npm run dev:mp-weixin
```

前端服务将在 http://localhost:5173 启动

### 4. 一键启动（推荐）

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

## 环境变量配置

### 后端 (.env)

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/rapport
SECRET_KEY=your-secret-key
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o
```

### 前端 (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 使用流程

1. 注册/登录账号
2. 创建联系人或直接记录对话
3. 粘贴对话文本，系统自动分析提取结构化信息
4. 在联系人详情页查看四层记忆模型
5. 导出Markdown文件备份

## 平台构建

### H5 构建
```bash
npm run build:h5
```

### 微信小程序构建
```bash
npm run build:mp-weixin
```

## 开发说明

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

### API文档

启动后端后访问 http://localhost:8000/docs 查看自动生成的API文档

## License

MIT
