# Rapport_v1.0_PRD

Rapport

## 1. 产品定位

- 面向用户：需要记录与维护人脉的人（活动、社交、商务会谈后复盘）
- 核心价值：把一段对话文本自动整理成 " 联系人长期记忆 "，方便下次快速接话与维护关系

## 2. MVP 目标（验收口径）

用户粘贴一段对话文本 -> 系统输出结构化长期记忆并保存 -> 用户可在联系人详情页回看，并可导出 Markdown。

> 本阶段仅支持文本输入，不做语音转写（ASR），不做文件上传。

## 3. 记忆结构（四层模型）

1. Identity（身份与稳定画像）
2. Status（当前状态与资源位）
3. Timeline（互动历史，递增追加）
4. Action Playbook（行动建议：送礼/续聊/合作/关系温度）

> 事实与推断分离：Identity/Status/Timeline 偏事实；Playbook 是建议，带置信度与证据引用（可选）。

## 4. 功能范围（MVP 仅做这些）

### 4.1 登录/注册（极简）

- 邮箱 + 密码注册/登录（弱校验，MVP 不做邮箱验证）

### 4.2 文本输入（核心）

- 页面提供一个大文本框：粘贴 " 我与某人的对话内容 "
- 可选输入：对方姓名（用户知道就填，不知道可空）
- 提交后：
  - 创建一条 meeting 记录（status=processing）
  - 调用 LLM 结构化抽取（输出符合 schema 的 JSON）
  - 匹配联系人：有姓名则优先匹配，否则新建联系人
  - 保存到 DB：contact + meeting + action_playbook
  - 返回结果并展示

### 4.3 联系人列表

- 展示：姓名、公司/岗位（若有）、最近会谈时间
- 支持搜索：按姓名关键词（先做最简单）

### 4.4 联系人详情页

- 展示四层模型：
  - Identity
  - Status
  - Timeline（会谈列表，按时间倒序）
  - Action Playbook（送礼/续聊/合作/关系温度）
- 每次新增会谈会追加到 Timeline，并更新 Playbook

### 4.5 导出（只做 Markdown）

- 在联系人详情页：一键导出该联系人的 Markdown
- 内容顺序：Identity -> Status -> Timeline -> Action Playbook

## 5. 非功能需求（MVP）

- LLM 输出必须可解析为 JSON（schema 校验，失败自动重试 1~2 次）
- 失败可见：meeting.status=failed + error_message
- 安全底线：密码加密存储；API key（如果有）加密存储

## 6. 技术实现

- 前端：先只做 Web（uni-app 的 H5 或直接普通 Web 均可）pnpm
- 后端：FastAPI + Mysql + uv
- 队列：MVP 可先同步调用（文本通常较快)
- LLM：先接入一个 OpenAI-compatible client（方便未来扩展国内外）
