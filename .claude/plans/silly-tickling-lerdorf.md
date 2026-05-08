# BridgeWatch AI Phase 2 — 后端最小可用版本实施计划

## Context

BridgeWatch AI 是一个桥梁隧道风险智能监测系统。前端 7 个页面（总览、事件中心、视频回放、普通桥梁、船撞融合、隧道、模型运维）已完成高保真演示版，数据全部基于 mock。下一步目标是建设后端服务，打通"前端 → 后端 API → 数据库"的最小闭环，**替换全部 mock 数据**。

基础资产已就位：
- 11 个 API 端点详细规范 → `reference source/02_接口详细文档.md`
- 8 张 PostgreSQL 表 DDL → `reference source/03_数据库建表SQL.md`
- 前端 TypeScript 类型 → `bridgewatch-ai/src/types.ts`
- 后端选型：**FastAPI (Python)** ✓ 已确认

---

## 实施路线图（4 周计划）

### 第 1 周：基础设施搭建

| 天 | 内容 | 交付物 |
|---|---|---|
| Day 1 | FastAPI 工程脚手架、config、docker-compose.yml (PostgreSQL + Redis) | `backend/app/main.py`, `config.py`, `docker-compose.yml` |
| Day 2 | SQLAlchemy async ORM 8 张模型、Alembic 初始迁移 | `backend/app/models/*.py`, `alembic/versions/0001_*` |
| Day 3 | 工具层：统一响应格式、异常处理、ID 生成器、分页工具、枚举 | `backend/app/utils/*.py` |
| Day 4 | Pydantic schemas：所有 API 请求/响应模型 | `backend/app/schemas/*.py` |
| Day 5 | 中间件（日志、软鉴权）、健康检查、路由注册、种子数据脚本 | `backend/app/middleware/*.py`, `seed/seed_data.py` |

### 第 2 周：核心 API 开发

| 天 | 内容 | 关键端点 |
|---|---|---|
| Day 6 | 对象列表 + 字典查询 API | `GET /api/objects`, `GET /api/dicts/{dict_type}` |
| Day 7 | 视频 API（列表、事件标记、播放地址） | `GET /api/videos`, `/videos/{id}/events`, `/videos/{id}/play-url` |
| Day 8 | 事件列表 + 详情（含多条件组合查询） | `GET /api/events`, `/events/{id}` |
| Day 9 | 事件复核 + Excel 导出 | `POST /api/events/{id}/review`, `/events/export` |
| Day 10 | 推理任务 API + pytest 测试框架 | `POST/GET /api/tasks/inference` |

### 第 3 周：看板统计 + 专题 + 联调

| 天 | 内容 | 交付物 |
|---|---|---|
| Day 11-12 | 三大看板接口（汇总、趋势、分布） | `GET /api/dashboard/*` (3 个端点) |
| Day 13 | 专题接口（普通桥梁统计、船撞融合） | `GET /api/topics/*` (2 个端点) |
| Day 14 | 扩种种子数据（20+ 事件、多种场景） | `seed/seed_data.py` 完善 |
| Day 15 | 集成测试、边界情况修复 | `backend/tests/*.py` |

### 第 4 周：前端对接 + Docker 部署

| 天 | 内容 | 交付物 |
|---|---|---|
| Day 16-17 | 前端 API 客户端 + API 类型定义 + 中英文枚举映射 | `bridgewatch-ai/src/lib/api.ts`, `type-mappers.ts`, `api-types.ts` |
| Day 18 | React Query hooks 封装（5 个 hook 文件） | `bridgewatch-ai/src/hooks/use-*.ts` |
| Day 19 | App.tsx 改造：mock 数据替换为真实 API 调用，加 loading/error 状态 | 修改 `App.tsx`, `vite.config.ts` |
| Day 20 | Docker 多阶段构建、部署脚本、最终联调 | `Dockerfile`, `docker-compose.yml` 完善 |

---

## 关键架构决策

### 后端
- **框架**: FastAPI + Uvicorn
- **ORM**: SQLAlchemy 2.0 async + asyncpg
- **迁移**: Alembic async 配置
- **配置**: pydantic-settings 加载环境变量
- **认证**: Phase 2 软鉴权（不阻塞请求，默认返回 admin 上下文）
- **项目结构**: `models/` → `schemas/` → `services/` → `api/` 四层清晰分离

### 前后端对接策略
- **中英文枚举映射**: API 用英文 (`"high"`, `"day"`, `"pending"`)，前端展示用中文 (`"高"`, `"白天"`, `"待复核"`)，通过 `type-mappers.ts` 集中转换
- **API 代理**: Vite dev server 代理 `/api` → `localhost:8000`，开发期零 CORS 问题
- **数据流变化**: 从 `import events from mockData` 改为 `useEventList() hook → apiClient.get('/events') → type-mapper → 组件 props`
- **React Query**: 统一管理请求缓存、loading/error 状态、自动重试

---

## 需要创建/修改的关键文件

### 新建后端文件 (~40 个)
- `backend/app/main.py` — FastAPI 应用工厂
- `backend/app/*.py` — config/database/middleware/utils 基础层
- `backend/app/models/*.py` — 8 个 ORM 模型
- `backend/app/schemas/*.py` — 7 个模块的 Pydantic schemas
- `backend/app/services/*.py` — 7 个业务服务层
- `backend/app/api/*.py` — 10 个路由模块
- `backend/app/seed/*.py` — 种子数据
- `backend/tests/*.py` — 集成测试
- `backend/Dockerfile`, `docker-compose.yml` — 部署

### 新建前端文件 (~10 个)
- `bridgewatch-ai/src/lib/api.ts` — API 客户端
- `bridgewatch-ai/src/lib/api-types.ts` — API 类型定义  
- `bridgewatch-ai/src/lib/type-mappers.ts` — 类型映射器
- `bridgewatch-ai/src/lib/query-provider.tsx` — React Query Provider
- `bridgewatch-ai/src/hooks/use-dashboard.ts` — 5 个数据 hooks

### 修改前端文件 (~3 个)
- `bridgewatch-ai/src/App.tsx` — 替换 mock 数据为 hooks
- `bridgewatch-ai/vite.config.ts` — 添加 API 代理
- `bridgewatch-ai/package.json` — 添加 `@tanstack/react-query`

---

## 验证方式

1. **后端**: `docker-compose up` 启动后，访问 `http://localhost:8000/docs` 查看 Swagger UI，逐个调用 11 个端点验证
2. **种子数据**: 运行种子脚本后，数据库应包含 3+ 桥梁/隧道对象、10+ 视频、20+ 事件
3. **前端联调**: `npm run dev` 启动前端，页面应展示真实数据而非 mock，无 404/500 错误
4. **端到端**: 事件筛选→详情→复核→确认的完整操作闭环可正常跑通
