/**
 * Type mappers: converts backend API types (English enums) to frontend display types (Chinese enums).
 *
 * Backend stores values in English (e.g. "high", "day", "pending")
 * Frontend displays values in Chinese (e.g. "高", "白天", "待复核")
 */

import type { EventRecord, RiskLevel, SceneType, ReviewStatus, ObjectType } from "../types";
import type { EventApiItem } from "./api";

// --- Enum mappers ---

export function mapRiskLevel(level: string): RiskLevel {
  const mapping: Record<string, RiskLevel> = {
    high: "高",
    medium: "中",
    low: "低",
  };
  return mapping[level] ?? "中";
}

export function mapSceneType(scene: string | null): SceneType {
  const mapping: Record<string, SceneType> = {
    day: "白天",
    night: "夜间",
    rain_fog: "雨雾",
  };
  return mapping[scene ?? ""] ?? "白天";
}

export function mapReviewStatus(status: string): ReviewStatus {
  const mapping: Record<string, ReviewStatus> = {
    pending: "待复核",
    reviewed: "已确认",
  };
  return mapping[status] ?? "待复核";
}

export function mapObjectType(type: string): string {
  const mapping: Record<string, string> = {
    bridge: "桥梁",
    tunnel: "隧道",
  };
  return mapping[type] ?? type;
}

function formatSeconds(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function formatClipRange(start: number, end: number): string {
  return `${formatSeconds(start)} - ${formatSeconds(end)}`;
}

// --- Event type mapper ---

export function mapEventApiToRecord(api: EventApiItem): EventRecord {
  // Generate a title from event type
  const eventTypeLabels: Record<string, string> = {
    collapse: "桥梁坍塌",
    deformation: "桥面大变形",
    congestion: "车辆积压",
    fire: "桥面火灾",
    ship_collision: "船舶碰撞",
  };

  // Infer object type from event_type (bridge events are most common)
  // TODO: enrich with actual object_type from API once events endpoint includes it
  const objectTypeMap: Record<string, ObjectType> = {
    collapse: "普通桥梁",
    deformation: "普通桥梁",
    congestion: "普通桥梁",
    fire: "普通桥梁",
    ship_collision: "长大桥梁",
  };

  return {
    id: api.event_id,
    objectName: api.object_name ?? api.object_id,
    objectType: objectTypeMap[api.event_type] ?? "普通桥梁",
    type: api.event_type as EventRecord["type"],
    title: eventTypeLabels[api.event_type] ?? api.event_type,
    riskLevel: mapRiskLevel(api.risk_level),
    scene: mapSceneType(api.scene_type),
    time: api.event_time,
    camera: api.video_name ?? "",
    confidence: api.risk_level === "high" ? 98 : api.risk_level === "medium" ? 85 : 72,
    clipRange: formatClipRange(api.start_second, api.end_second),
    sensorSignal: api.result_desc ?? "",
    status: mapReviewStatus(api.review_status),
    description: api.result_desc ?? "",
    // Overlays are empty for API data — populated later with algorithm results
    overlays: [],
  };
}

export function mapEventsApiToRecords(apiEvents: EventApiItem[]): EventRecord[] {
  return apiEvents.map(mapEventApiToRecord);
}
