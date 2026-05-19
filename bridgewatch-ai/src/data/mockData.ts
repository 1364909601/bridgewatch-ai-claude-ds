import type {
  DashboardMetric,
  EventRecord,
  FusionFactor,
  LoadPoint,
  ModelVersion,
  MonitoringPoint,
  NavItem,
  PageId,
  RadarPoint,
  SceneAssessmentPoint,
  TaskRun,
  TrendPoint,
  TunnelMetricPoint
} from "../types";

export const navItems: NavItem[] = [
  { id: "overview", label: "总览指挥台", eyebrow: "Overview" },
  { id: "events", label: "事件中心", eyebrow: "Risk Events" },
  { id: "ordinary", label: "普通桥梁", eyebrow: "Ordinary Bridge" },
  { id: "playback", label: "视频回放", eyebrow: "Playback" },
  { id: "ship", label: "船撞融合", eyebrow: "Ship Fusion" },
  { id: "tunnel", label: "隧道专题", eyebrow: "Tunnel" },
  { id: "ops", label: "模型运维", eyebrow: "Model Ops" },
  { id: "reports", label: "报告中心", eyebrow: "Reports" },
  { id: "settings", label: "系统设置", eyebrow: "Settings" },
  { id: "audit", label: "审计日志", eyebrow: "Audit" }
];

export const overviewMetrics: DashboardMetric[] = [
  { id: "high", label: "高风险事件", value: "3", hint: "需要立即复核", tone: "danger" },
  { id: "medium", label: "中风险事件", value: "7", hint: "需要持续关注", tone: "warning" },
  { id: "low", label: "低风险事件", value: "12", hint: "维持自动巡检", tone: "low" },
  { id: "monitored", label: "监测对象", value: "28", hint: "桥梁与隧道总数", tone: "info" }
];

export const systemStats = [
  { label: "传感器在线率", value: "96.8%", status: "正常" },
  { label: "视频设备在线率", value: "94.2%", status: "正常" },
  { label: "数据采集率", value: "98.1%", status: "正常" },
  { label: "AI 分析稳定度", value: "92.7%", status: "稳定" }
];

export const trendSeries: TrendPoint[] = [
  { label: "14:28", incidents: 3, strainIndex: 62, anomalies: 2 },
  { label: "14:29", incidents: 4, strainIndex: 66, anomalies: 2 },
  { label: "14:30", incidents: 6, strainIndex: 71, anomalies: 3 },
  { label: "14:31", incidents: 5, strainIndex: 68, anomalies: 2 },
  { label: "14:32", incidents: 7, strainIndex: 78, anomalies: 4 }
];

export const loadSeries: LoadPoint[] = [
  { zone: "西锚碇", load: 2156, vibration: 42 },
  { zone: "主塔", load: 2456, vibration: 58 },
  { zone: "东主塔", load: 2089, vibration: 44 },
  { zone: "东锚碇", load: 1845, vibration: 31 }
];

export const events: EventRecord[] = [
  {
    id: "EV-001",
    objectName: "南京长江大桥 #B-001",
    objectType: "长大桥梁",
    title: "桥体坍塌风险",
    type: "坍塌风险",
    riskLevel: "高",
    confidence: 97,
    scene: "白天",
    time: "14:31:45",
    camera: "UAV-03",
    clipRange: "02:11 - 02:28",
    status: "待复核",
    sensorSignal: "结构挠度异常，应变峰值上升 18%",
    description: "桥面局部几何形态发生突变，视频识别与 SHM 应变曲线同时触发高风险阈值。",
    overlays: [{ id: "o1", label: "桥面异常", left: 37, top: 42, width: 24, height: 14 }]
  },
  {
    id: "EV-023",
    objectName: "杭州湾跨海大桥 #B-023",
    objectType: "长大桥梁",
    title: "桥面变形异常",
    type: "桥面变形",
    riskLevel: "中",
    confidence: 91,
    scene: "雨雾",
    time: "14:30:22",
    camera: "UAV-08",
    clipRange: "01:06 - 01:24",
    status: "待复核",
    sensorSignal: "轮廓偏移 14px，桥端挠度接近阈值",
    description: "连续帧中桥面边缘曲率异常，雨雾场景下置信度略低，需要人工复核。",
    overlays: [{ id: "o2", label: "变形段", left: 29, top: 48, width: 31, height: 11 }]
  },
  {
    id: "EV-015",
    objectName: "青岛胶州湾大桥 #B-015",
    objectType: "普通桥梁",
    title: "车辆拥堵",
    type: "车辆积压",
    riskLevel: "低",
    confidence: 88,
    scene: "白天",
    time: "14:29:18",
    camera: "UAV-12",
    clipRange: "03:44 - 04:02",
    status: "已确认",
    sensorSignal: "车流密度 0.76，平均速度 18km/h",
    description: "车流速度下降但未达到高风险阈值，建议持续观察。",
    overlays: [{ id: "o3", label: "拥堵区域", left: 18, top: 54, width: 42, height: 16 }]
  },
  {
    id: "EV-008",
    objectName: "厦门演武大桥 #B-008",
    objectType: "普通桥梁",
    title: "桥面火情",
    type: "桥面火灾",
    riskLevel: "高",
    confidence: 95,
    scene: "夜间",
    time: "14:28:05",
    camera: "UAV-07",
    clipRange: "00:51 - 01:09",
    status: "待复核",
    sensorSignal: "热源温升 +42℃，烟雾区域持续扩大",
    description: "可见光与热源特征同时触发，事件应进入应急复核队列。",
    overlays: [{ id: "o4", label: "明火区域", left: 58, top: 45, width: 16, height: 20 }]
  },
  {
    id: "EV-002",
    objectName: "上海长江大桥 #B-002",
    objectType: "长大桥梁",
    title: "船舶碰撞风险",
    type: "船撞风险",
    riskLevel: "中",
    confidence: 94,
    scene: "白天",
    time: "14:27:33",
    camera: "UAV-10",
    clipRange: "04:02 - 04:24",
    status: "待复核",
    sensorSignal: "AIS 偏航 +3.2°，通航净空 32.5m",
    description: "船舶接近桥墩保护区，视频轨迹与 AIS 偏航同时抬升。",
    overlays: [
      { id: "o5", label: "目标船舶", left: 23, top: 59, width: 19, height: 12 },
      { id: "o6", label: "桥墩保护区", left: 55, top: 26, width: 13, height: 41 }
    ]
  },
  {
    id: "EV-044",
    objectName: "海沧隧道 #T-009",
    objectType: "隧道",
    title: "隧道烟雾异常",
    type: "烟雾预警",
    riskLevel: "中",
    confidence: 90,
    scene: "夜间",
    time: "14:26:19",
    camera: "UAV-15",
    clipRange: "01:42 - 01:59",
    status: "待复核",
    sensorSignal: "CO 指数抬升 15%，照度下降 22%",
    description: "视频烟雾特征与环境监测异常同时出现，建议进入联动复核流程。",
    overlays: [{ id: "o7", label: "烟雾区域", left: 44, top: 33, width: 20, height: 24 }]
  }
];

export const sceneAssessment: SceneAssessmentPoint[] = [
  { metric: "坍塌识别", day: 96, night: 89, fog: 83 },
  { metric: "桥面变形", day: 93, night: 86, fog: 79 },
  { metric: "车辆积压", day: 97, night: 92, fog: 88 },
  { metric: "桥面火灾", day: 95, night: 94, fog: 86 }
];

export const readinessRadar: RadarPoint[] = [
  { subject: "坍塌", score: 91 },
  { subject: "变形", score: 87 },
  { subject: "拥堵", score: 95 },
  { subject: "火灾", score: 93 },
  { subject: "夜雨", score: 82 }
];

export const shipMonitoringSeries: MonitoringPoint[] = [
  { label: "14:28", impact: 12, strain: 34, clearance: 88 },
  { label: "14:29", impact: 16, strain: 38, clearance: 74 },
  { label: "14:30", impact: 22, strain: 42, clearance: 63 },
  { label: "14:31", impact: 36, strain: 55, clearance: 54 },
  { label: "14:32", impact: 48, strain: 64, clearance: 47 }
];

export const fusionFactors: FusionFactor[] = [
  { label: "AIS 接近度", score: 34, note: "进入一级保护圈" },
  { label: "视频净距估计", score: 26, note: "净距低于 60m" },
  { label: "应变峰值", score: 21, note: "相对基线上升 18%" },
  { label: "振动异常", score: 11, note: "桥墩瞬时振动抬升" }
];

export const tunnelSeries: TunnelMetricPoint[] = [
  { label: "14:28", coIndex: 42, lux: 156, traffic: 1256 },
  { label: "14:29", coIndex: 45, lux: 151, traffic: 1198 },
  { label: "14:30", coIndex: 51, lux: 143, traffic: 1082 },
  { label: "14:31", coIndex: 58, lux: 131, traffic: 986 },
  { label: "14:32", coIndex: 49, lux: 138, traffic: 1034 }
];

export const modelVersions: ModelVersion[] = [
  { name: "BridgeWatch Vision", version: "v1.4.2", scope: "普通桥梁四类事件", status: "在线", updatedAt: "14:20:13" },
  { name: "Ship Collision Fusion", version: "v0.8.6", scope: "船撞融合原型", status: "验证中", updatedAt: "14:12:50" },
  { name: "Tunnel Guard", version: "v0.6.1", scope: "隧道融合原型", status: "候选", updatedAt: "13:58:31" }
];

export const taskRuns: TaskRun[] = [
  { name: "UAV 批量推理", status: "运行中", progress: 74, startedAt: "14:28", eta: "14:36" },
  { name: "夜雨样本重评", status: "排队中", progress: 18, startedAt: "14:29", eta: "14:42" },
  { name: "SHM 数据对齐", status: "成功", progress: 100, startedAt: "14:10", eta: "已完成" },
  { name: "隧道联动回放", status: "失败", progress: 100, startedAt: "13:48", eta: "需要重试" }
];

export const shipTrack = [
  { label: "船舶 A", x: 30, y: 150 },
  { label: "船舶 A", x: 60, y: 130 },
  { label: "船舶 A", x: 100, y: 110 },
  { label: "船舶 A", x: 130, y: 90 },
  { label: "船舶 A", x: 180, y: 60 }
];

export const videoFeeds = [
  { name: "南京长江大桥 #B-001", state: "稳定", tone: "ok" },
  { name: "杭州湾跨海大桥 #B-023", state: "形变关注", tone: "warning" },
  { name: "厦门演武大桥 #B-008", state: "火情复核", tone: "danger" },
  { name: "海沧隧道 #T-009", state: "低能见度", tone: "low" }
] as const;

export const pageObjectives: Record<PageId, string> = {
  overview: "综合查看普通桥梁、长大桥梁与隧道的风险态势，并提供值守汇报入口。",
  events: "快速检索和复核风险事件，决定是否进入人工处置流程。",
  playback: "通过关键片段完成事件复盘，并核对识别框与传感器关联。",
  ordinary: "展示普通桥梁四类风险模型的能力、场景差异与典型案例。",
  ship: "联动视频、AIS 与 SHM 指标，呈现船撞融合预警链路。",
  tunnel: "结合视频与环境监测数据，演示隧道异常识别与联动判断。",
  ops: "查看模型版本、推理任务与工程运行健康度。",
  reports: "生成和导出系统运行报告、事件统计报表。",
  settings: "管理系统配置、用户权限与系统参数。",
  audit: "查看系统操作审计日志，追踪关键操作记录。"
};

export const pageHighlights: Record<PageId, string[]> = {
  overview: ["当前高风险事件 3 条，集中在坍塌风险与桥面火情。", "SHM 数据流在线率 96.8%。", "AI 分析引擎处于实时生成摘要状态。"],
  events: ["待复核队列按高风险优先排序。", "桥面火情和坍塌风险需要优先人工确认。", "事件详情可直接跳转视频回放。"],
  playback: ["当前页面用于演示识别框叠加与关键时间窗。", "回放轴需突出风险片段和相关事件。", "适合用于现场复盘或汇报。"],
  ordinary: ["普通桥梁四类事件已具备演示闭环。", "夜间和雨雾场景仍是重点优化方向。", "车辆积压识别稳定性最高。"],
  ship: ["船舶接近保护区时需联动 AIS、视频与 SHM 曲线。", "当前原型强调可解释融合评分。", "页面重点展示船撞预警链路。"],
  tunnel: ["隧道异常以空气质量、照度和交通流为主。", "视频与监测数据共同支撑风险判断。", "专题页保留异常案例与趋势曲线。"],
  ops: ["普通桥梁模型已在线运行。", "船撞与隧道模型处于原型验证阶段。", "失败任务需要快速重试或人工介入。"],
  reports: ["报告中心提供事件统计、风险趋势和系统运行报告。", "支持数据导出和定期报告生成。", "可按时间范围和事件类型筛选。"],
  settings: ["管理系统用户和角色权限。", "配置系统运行参数和告警规则。", "查看系统日志和操作审计。"],
  audit: ["查看系统操作审计日志。", "按类型和时间筛选审计记录。", "追踪关键操作的用户和详情。"]
};
