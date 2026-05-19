export type PageId =
  | "overview"
  | "events"
  | "playback"
  | "ordinary"
  | "ship"
  | "tunnel"
  | "ops"
  | "reports"
  | "settings"
  | "audit";

export type ObjectType = "普通桥梁" | "长大桥梁" | "隧道";
export type RiskLevel = "高" | "中" | "低";
export type SceneType = "白天" | "夜间" | "雨雾";
export type ReviewStatus = "待复核" | "已确认";
export type ModelStatus = "在线" | "候选" | "验证中";
export type TaskStatus = "运行中" | "排队中" | "成功" | "失败";

export interface NavItem {
  id: PageId;
  label: string;
  eyebrow: string;
}

export interface DashboardMetric {
  id: string;
  label: string;
  value: string;
  unit?: string;
  hint: string;
  tone: "danger" | "warning" | "low" | "info" | "ok";
}

export interface EventOverlay {
  id: string;
  label: string;
  left: number;
  top: number;
  width: number;
  height: number;
}

export interface EventRecord {
  id: string;
  objectName: string;
  objectType: ObjectType;
  title: string;
  type: string;
  riskLevel: RiskLevel;
  confidence: number;
  scene: SceneType;
  time: string;
  camera: string;
  clipRange: string;
  status: ReviewStatus;
  sensorSignal: string;
  description: string;
  overlays: EventOverlay[];
}

export interface TrendPoint {
  label: string;
  incidents: number;
  strainIndex: number;
  anomalies: number;
}

export interface LoadPoint {
  zone: string;
  load: number;
  vibration: number;
}

export interface SceneAssessmentPoint {
  metric: string;
  day: number;
  night: number;
  fog: number;
}

export interface RadarPoint {
  subject: string;
  score: number;
}

export interface MonitoringPoint {
  label: string;
  impact: number;
  strain: number;
  clearance: number;
}

export interface FusionFactor {
  label: string;
  score: number;
  note: string;
}

export interface TunnelMetricPoint {
  label: string;
  coIndex: number;
  lux: number;
  traffic: number;
}

export interface ModelVersion {
  name: string;
  version: string;
  scope: string;
  status: ModelStatus;
  updatedAt: string;
}

export interface TaskRun {
  name: string;
  status: TaskStatus;
  progress: number;
  startedAt: string;
  eta: string;
}

export interface OperationsDigest {
  headline: string;
  bullets: string[];
  source: "mock" | "gemini" | "fallback";
  generatedAt: string;
}

export interface DigestRequest {
  pageId: PageId;
  pageTitle: string;
  pageObjective: string;
  highlights: string[];
  selectedEvent?: EventRecord;
}
