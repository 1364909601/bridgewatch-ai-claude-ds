# BridgeWatch AI

**桥隧基础设施智能监测系统** — AI 驱动的桥梁与隧道重大风险识别平台。

基于实时视频分析、传感器数据融合，对普通桥梁（坍塌/变形/积压/火灾）、长大桥梁（船撞融合）和隧道（环境联动预警）进行全天候智能监测。

---

## 项目结构

```
├── bridgewatch-ai/              # 前端 — React 19 + Vite + TypeScript + Tailwind v4
│   ├── src/
│   │   ├── pages/               # 7 个业务页面
│   │   ├── components/          # 8 个通用组件（含 AlertBell）
│   │   ├── hooks/               # React Query hooks（8 个领域模块）
│   │   ├── contexts/            # AuthContext（JWT 认证状态管理）
│   │   ├── lib/                 # API 客户端 + 类型映射器 + auth 工具
│   │   └── data/                # Mock 数据（离线回退）
│   └── Dockerfile               # 多阶段构建（node build → nginx serve）
├── backend/                     # 后端 — FastAPI + SQLAlchemy async + PostgreSQL/SQLite
│   ├── app/
│   │   ├── api/                 # 20+ RESTful API 端点
│   │   ├── models/              # 9 张表的 ORM 模型
│   │   ├── services/            # 业务逻辑层（9 个 Service）
│   │   ├── engine/              # 检测推理引擎（6 个检测器 + Worker）
│   │   ├── middleware/          # 日志 + JWT 鉴权 + Prometheus 中间件
│   │   ├── monitoring/          # Prometheus 指标注册
│   │   ├── utils/               # 响应格式/异常/分页/ID 生成
│   │   └── seed/                # 种子数据脚本
│   ├── tests/                   # pytest 测试（13 个用例）
│   ├── alembic/
│   ├── Dockerfile
│   └── docker-compose.yml       # PostgreSQL + Redis + 后端 + 前端 + Prometheus + Grafana
├── nginx/                       # Nginx 反向代理配置
├── prometheus/                  # Prometheus 抓取配置
├── 桥梁与隧道重大风险智能识别_PRD.md
└── 项目计划开发文档.md
```

---

## 当前进展

| 阶段 | 状态 | 核心内容 |
|------|------|----------|
| Phase 1 — 前端演示版 | ✅ 完成 | 7 页面 + 8 组件 + 深色驾驶舱 UI |
| Phase 2 — 后端 MVP | ✅ 完成 | 20+ API + 9 ORM 模型 + DB 迁移 + Docker |
| Phase 3 — 前后端联调 | ✅ 完成 | SQLite 开发模式，OverviewPage/EventCenter 数据对接 |
| Phase 4 — 算法推理管线 | ✅ 完成 | 四类桥梁 + 船撞 + 隧道检测引擎 + 告警通知闭环 |
| Phase 5 — 用户权限 | ✅ 完成 | JWT 认证 + 3 角色（admin/operator/viewer）+ 登录页 |
| Phase 6 — 上线交付 | 🔄 75% | Nginx + Docker 编排 + Prometheus/Grafana + pytest

| 层 | 技术 |
|------|------|
| 前端框架 | React 19 + TypeScript |
| 构建工具 | Vite 8 |
| 样式 | Tailwind CSS v4 + 自定义 CSS |
| 图表/动画 | Recharts + Framer Motion |
| 状态管理 | @tanstack/react-query |
| 后端框架 | FastAPI (Python 3.13) |
| ORM | SQLAlchemy 2.0 async |
| 数据库 | PostgreSQL 16（生产）/ SQLite（开发） |
| 认证 | JWT (python-jose) + bcrypt |
| 监控 | Prometheus + Grafana |
| CI/测试 | pytest + GitHub Actions |
| 部署 | Docker + docker-compose + Nginx |

---

## 快速启动

### 开发模式（SQLite）

```bash
# 后端
cd backend
pip install -r requirements.txt
# 确保已安装 aiosqlite: pip install aiosqlite
cp .env.example .env   # 修改 DATABASE_URL 为 sqlite+aiosqlite:///./bridgewatch.db
python run.py          # 启动于 localhost:8000

# 种子数据（新开终端）
cd backend
python -m app.seed.seed_data

# 前端（新开终端）
cd bridgewatch-ai
npm install
npm run dev            # 启动于 localhost:5173
```

浏览器打开 `http://localhost:5173`，前端自动检测后端并切换到实时数据模式。

### 生产模式（PostgreSQL + Docker）

```bash
cd backend
docker-compose up -d
```

---

## API 概览

| 端点 | 说明 |
|------|------|
| `GET /api/health` | 健康检查 |
| `GET /api/objects` | 监测对象列表 |
| `GET /api/dicts/{type}` | 枚举字典 |
| `GET /api/dashboard/summary` | 看板聚合统计 |
| `GET /api/dashboard/trend` | 事件趋势 |
| `GET /api/dashboard/distribution` | 事件类型分布 |
| `GET /api/events` | 事件列表（多条件筛选+分页） |
| `GET /api/events/{id}` | 事件详情 |
| `POST /api/events/{id}/review` | 事件复核 |
| `GET /api/videos` | 视频列表 |
| `POST /api/tasks/inference` | 创建推理任务 |

完整 API 文档在 `http://localhost:8000/docs`（Swagger UI）。

---

## 相关文档

- [项目计划开发文档](./bridgewatch-ai/项目计划开发文档.md)
- [待开发模块文档](./bridgewatch-ai/待开发模块文档.md)
- [PRD 文档](./桥梁与隧道重大风险智能识别_PRD.md)
- [研发任务拆解](./研发任务拆解表.md)
- [接口详细文档](./reference%20source/02_接口详细文档.md)
- [算法技术方案](./reference%20source/04_算法技术方案.md)
