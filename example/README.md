# 虚拟示例数据

本目录包含 BridgeWatch AI 系统的虚拟示例数据，覆盖前端所有页面和功能所需的全部数据结构。

## 文件说明

| 文件 | 对应页面 | 数据内容 |
|------|----------|----------|
| `events.json` | 事件中心、视频回放、普通桥梁、隧道 | 事件记录、风险分类、叠加框、分页摘要 |
| `dashboard.json` | 总览指挥台 | 指标卡片、系统状态、趋势图、荷载分布、视频摘要、API 统计 |
| `monitoring.json` | 船撞融合、隧道专题、普通桥梁 | 船迹、融合评分、环境监测、场景识别、模型雷达 |
| `models.json` | 模型运维 | 模型版本、任务执行、后端 API 模型/任务 |
| `navigation.json` | 全局导航、AI 摘要 | 导航菜单、页面目标、高亮要点、AI 摘要示例 |
| `api-responses.json` | 全部 API 联调 | 完整后端 API 响应格式示例（16 端点） |

## 数据结构说明

所有数据与前端 TypeScript 类型定义（`src/types.ts`）一一对应：

- **EventRecord** → `events.json` → 事件中心 / 回放页面
- **DashboardMetric / TrendPoint / LoadPoint** → `dashboard.json` → 总览页面
- **MonitoringPoint / FusionFactor** → `monitoring.json` → 船撞融合页面
- **TunnelMetricPoint** → `monitoring.json` → 隧道页面
- **SceneAssessmentPoint / RadarPoint** → `monitoring.json` → 普通桥梁页面
- **ModelVersion / TaskRun** → `models.json` → 模型运维页面
- **ApiResponse\<T\> / PaginatedResponse\<T\>** → `api-responses.json` → 后端对接

## 用法

### 前端 mock 数据替换

将对应 JSON 文件中的数据复制到 `bridgewatch-ai/src/data/mockData.ts` 中对应数组即可。

### 后端种子数据

运行 `cd backend && python -m app.seed.seed_data` 即可将类似数据写入数据库。

### API 文档参考

`api-responses.json` 提供了后端 16 个端点的完整请求/响应示例，适合用于接口联调和测试。

## 数据覆盖清单

- [x] 8 条事件（覆盖高/中/低风险、普通桥梁/长大桥梁/隧道、白天/夜间/雨雾）
- [x] 5 个监测对象（3 桥梁 + 2 隧道）
- [x] 8 条视频记录
- [x] 4 个场景识别指标（坍塌/变形/积压/火灾）
- [x] 5 个雷达维度
- [x] 4 个融合因子 + 船迹
- [x] 5 个模型版本 + 6 个任务
- [x] 4 个视频摘要卡片
- [x] 完整的 API 响应封装格式
