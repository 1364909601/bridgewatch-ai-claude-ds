/**
 * BridgeWatch AI API Client
 *
 * Centralized API client for communicating with the FastAPI backend.
 * All functions return typed promises.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

// --- Response types from backend ---

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T | null;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  total: number;
  page_no: number;
  page_size: number;
  list: T[];
}

// --- Domain types (mirrors backend API schemas) ---

export interface ObjectApiItem {
  object_id: string;
  object_name: string;
  object_type: string;
  location_desc: string | null;
  status: string;
}

export interface DictItem {
  value: string;
  label: string;
}

export interface EventApiItem {
  event_id: string;
  object_id: string;
  object_name?: string;
  video_id: string;
  video_name?: string;
  event_type: string;
  risk_level: string;
  scene_type: string | null;
  event_time: string;
  start_second: number;
  end_second: number;
  thumbnail_url: string | null;
  clip_url?: string | null;
  result_desc: string | null;
  review_status: string;
  review_remark: string | null;
  created_time?: string;
  updated_time?: string;
}

export interface DashboardSummary {
  total: number;
  high_risk: number;
  medium_risk: number;
  low_risk: number;
  bridges: number;
  tunnels: number;
  total_objects: number;
}

export interface TrendPoint {
  date: string;
  count: number;
  high_risk: number;
}

export interface DistributionItem {
  event_type: string;
  event_type_name: string;
  count: number;
}

export interface VideoApiItem {
  video_id: string;
  object_id: string;
  video_name: string;
  file_url: string;
  capture_time: string;
  duration_seconds: number;
  resolution: string | null;
  scene_type: string | null;
  preprocess_status: string;
}

export interface VideoEventMark {
  event_id: string;
  event_type: string;
  risk_level: string;
  start_second: number;
  end_second: number;
}

export interface VideoPlayUrl {
  video_id: string;
  play_url: string;
  duration_seconds: number;
}

export interface TaskApiItem {
  task_id: string;
  video_id: string;
  model_id: string;
  task_name: string;
  task_status: string;
  start_time: string | null;
  end_time: string | null;
  result_summary: string | null;
  error_message: string | null;
  created_time: string;
}

export interface BridgeSummary {
  event_type_stats: { event_type: string; event_type_name: string; count: number }[];
  scene_stats: any[];
}

export interface FusionResultItem {
  fusion_id: string;
  score: number | null;
  risk_level: string;
  rule_desc: string | null;
  fusion_time: string;
  related_event_id: string | null;
}

// --- Events query params ---

export interface EventQueryParams {
  page_no?: number;
  page_size?: number;
  start_time?: string;
  end_time?: string;
  object_type?: string;
  object_id?: string;
  event_type?: string;
  risk_level?: string;
  scene_type?: string;
  review_status?: string;
  video_name?: string;
}

// --- API Client ---

class ApiError extends Error {
  constructor(
    public code: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function buildQuery(params: Record<string, any>): string {
  const parts: string[] = [];
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
    }
  }
  return parts.length ? `?${parts.join("&")}` : "";
}

async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  const body: ApiResponse<T> = await response.json();

  if (body.code !== 0) {
    throw new ApiError(body.code, body.message || "请求失败");
  }

  return body.data as T;
}

// --- Dashboard API ---

export function getDashboardSummary(params?: {
  start_time?: string;
  end_time?: string;
  object_type?: string;
  object_id?: string;
  scene_type?: string;
}) {
  return apiClient<DashboardSummary>(`/dashboard/summary${buildQuery(params || {})}`);
}

export function getDashboardTrend(days: number = 7) {
  return apiClient<TrendPoint[]>(`/dashboard/trend?days=${days}`);
}

export function getDashboardDistribution() {
  return apiClient<DistributionItem[]>("/dashboard/distribution");
}

// --- Events API ---

export function getEvents(params?: EventQueryParams) {
  return apiClient<PaginatedResponse<EventApiItem>>(
    `/events${buildQuery(params || {})}`
  );
}

export function getEventDetail(eventId: string) {
  return apiClient<EventApiItem>(`/events/${eventId}`);
}

export function reviewEvent(
  eventId: string,
  body: { review_status: string; review_remark?: string }
) {
  return apiClient<{ event_id: string; review_status: string; review_remark: string | null }>(
    `/events/${eventId}/review`,
    { method: "POST", body: JSON.stringify(body) }
  );
}

// --- Videos API ---

export function getVideos(params?: { page_no?: number; page_size?: number; object_id?: string; scene_type?: string }) {
  return apiClient<PaginatedResponse<VideoApiItem>>(`/videos${buildQuery(params || {})}`);
}

export function getVideoEvents(videoId: string) {
  return apiClient<VideoEventMark[]>(`/videos/${videoId}/events`);
}

export function getVideoPlayUrl(videoId: string) {
  return apiClient<VideoPlayUrl>(`/videos/${videoId}/play-url`);
}

// --- Tasks API ---

export function getInferenceTasks(params?: { page_no?: number; page_size?: number; task_status?: string; video_id?: string }) {
  return apiClient<PaginatedResponse<TaskApiItem>>(`/tasks/inference${buildQuery(params || {})}`);
}

export function createInferenceTask(body: { video_id: string; model_id: string; task_name?: string }) {
  return apiClient<TaskApiItem>("/tasks/inference", { method: "POST", body: JSON.stringify(body) });
}

// --- Topics API ---

export function getBridgeSummary(object_id?: string) {
  return apiClient<BridgeSummary>(`/topics/bridge/summary${buildQuery({ object_id })}`);
}

export function getShipCollisionFusion(params: { object_id: string; start_time?: string; end_time?: string }) {
  return apiClient<FusionResultItem[]>(`/topics/ship-collision/fusion${buildQuery(params)}`);
}

// --- Objects API ---

export function getObjects(params?: { object_type?: string; status?: string }) {
  return apiClient<ObjectApiItem[]>(`/objects${buildQuery(params || {})}`);
}

// --- Dicts API ---

export function getDicts(dictType: string) {
  return apiClient<DictItem[]>(`/dicts/${dictType}`);
}
