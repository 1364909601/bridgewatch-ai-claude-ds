import { useMemo } from "react";
import { Maximize2, Minus, Plus } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import type { PageId } from "../types";
import { MetricCard } from "../components/MetricCard";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";
import { useDashboardSummary } from "../hooks/use-dashboard";
import { useUnreadAlertCount } from "../hooks/use-alerts";
import { useMonitoringData } from "../hooks/use-monitoring";
import { useShipCollisionFusion } from "../hooks/use-topics";
import { useVideoList } from "../hooks/use-videos";

interface OverviewPageProps {
  onFocusEvent: (eventId: string, targetPage?: PageId) => void;
}

// ── Object IDs from seed data ────────────────────────────────────
const BRIDGE_ID = "OBJ-20260508-001";
const LARGE_BRIDGE_ID = "OBJ-20260508-003";
const TUNNEL_ID = "OBJ-20260508-004";

const SHM_TYPES = "displacement,vibration,water_level";
const TUNNEL_TYPES = "co,lux,traffic";

export function OverviewPage({ onFocusEvent }: OverviewPageProps) {
  // ── API hooks ────────────────────────────────────────────────────
  const { data: summary, isLoading: summaryLoading } = useDashboardSummary();
  const { data: unreadAlerts } = useUnreadAlertCount();
  const { data: shmData } = useMonitoringData(BRIDGE_ID, SHM_TYPES, { limit: 20 });
  const { data: tunnelData } = useMonitoringData(TUNNEL_ID, TUNNEL_TYPES, { limit: 30 });
  const { data: fusionData } = useShipCollisionFusion({ object_id: LARGE_BRIDGE_ID });
  const { data: videosData } = useVideoList({ page_size: 4 });

  // ── Derived data ─────────────────────────────────────────────────
  const metrics = useMemo(() => {
    if (summaryLoading) {
      return [
        { id: "high", label: "高风险事件", value: "—", hint: "加载中...", tone: "danger" as const },
        { id: "medium", label: "中风险事件", value: "—", hint: "加载中...", tone: "warning" as const },
        { id: "low", label: "低风险事件", value: "—", hint: "加载中...", tone: "low" as const },
        { id: "monitored", label: "监测对象", value: "—", hint: "加载中...", tone: "info" as const },
      ];
    }
    return [
      { id: "high", label: "高风险事件", value: String(summary?.high_risk ?? 0), hint: "需要立即复核", tone: "danger" as const },
      { id: "medium", label: "中风险事件", value: String(summary?.medium_risk ?? 0), hint: "需要持续关注", tone: "warning" as const },
      { id: "low", label: "低风险事件", value: String(summary?.low_risk ?? 0), hint: "维持自动巡检", tone: "low" as const },
      { id: "monitored", label: "监测对象", value: String(summary?.total_objects ?? 0), hint: "桥梁与隧道总数", tone: "info" as const },
    ];
  }, [summary, summaryLoading]);

  // System status from real data
  const sysStats = useMemo(() => [
    { label: "事件总数", value: String(summary?.total ?? 0), status: `${summary?.high_risk ?? 0} 条高风险` },
    { label: "未处理告警", value: String(unreadAlerts?.count ?? 0), status: unreadAlerts?.count ? "需要关注" : "全部已处理" },
    { label: "监测桥梁", value: String(summary?.bridges ?? 0), status: "已接入系统" },
    { label: "监测隧道", value: String(summary?.tunnels ?? 0), status: "已接入系统" },
  ], [summary, unreadAlerts]);

  // SHM data: group by data_type
  const shmPoints = useMemo(() => {
    if (!shmData?.length) return null;
    const latest: Record<string, { value: number; unit: string }> = {};
    for (const p of shmData) {
      latest[p.data_type] = { value: p.data_value, unit: p.data_type };
    }
    return latest;
  }, [shmData]);

  // Ship fusion latest result
  const latestFusion = useMemo(() => {
    if (!fusionData?.length) return null;
    return fusionData[0];
  }, [fusionData]);

  // Tunnel monitoring: latest values by type
  const tunnelLatest = useMemo(() => {
    if (!tunnelData?.length) return null;
    const groups: Record<string, number[]> = {};
    for (const p of tunnelData) {
      if (!groups[p.data_type]) groups[p.data_type] = [];
      groups[p.data_type].push(p.data_value);
    }
    const avg: Record<string, number> = {};
    for (const [k, vals] of Object.entries(groups)) {
      avg[k] = vals.reduce((a, b) => a + b, 0) / vals.length;
    }
    return avg;
  }, [tunnelData]);

  // Videos list
  const videoList = useMemo(() => videosData?.list ?? [], [videosData]);

  return (
    <div className="dashboard-stack">
      {/* ── Metric cards ──────────────────────────────────────────── */}
      <div className="risk-grid">
        {metrics.map((m) => <MetricCard key={m.id} metric={m} />)}
      </div>

      {/* ── Map + System status ──────────────────────────────────── */}
      <div className="dashboard-row main-row">
        <Panel
          title="监测对象分布"
          action={
            <div className="flex gap-2">
              <StatusPill tone="neutral">全部</StatusPill>
              <StatusPill tone="info">桥梁 {summary?.bridges ?? 0}</StatusPill>
              <StatusPill tone="low">隧道 {summary?.tunnels ?? 0}</StatusPill>
            </div>
          }
        >
          <div className="map-panel">
            <div className="map-label center">长大桥梁群</div>
            <div className="map-label left">普通桥梁群</div>
            <div className="map-label right">隧道监测带</div>
            <div className="map-pin danger p1" />
            <div className="map-pin warning p2" />
            <div className="map-pin ok p3" />
            <div className="map-tool">
              <button type="button" title="全屏"><Maximize2 size={16} /></button>
              <button type="button" title="放大"><Plus size={16} /></button>
              <button type="button" title="缩小"><Minus size={16} /></button>
            </div>
          </div>
        </Panel>

        <Panel title="系统状态总览">
          <div className="system-list">
            {sysStats.map((s) => (
              <div key={s.label} className="system-row">
                <div className="flex items-center gap-3">
                  <span className="green-dot" />
                  <div>
                    <strong>{s.label}</strong>
                    <div className="mt-1 text-sm text-slate-400">{s.status}</div>
                  </div>
                </div>
                <div className="text-right">
                  <strong>{s.value}</strong>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      {/* ── SHM monitoring ───────────────────────────────────────── */}
      <Panel title="结构健康监测 / 长江大桥">
        <div className="shm-grid">
          <MiniSignal
            title="振动监测"
            value={shmPoints?.vibration ? shmPoints.vibration.value.toFixed(3) : "—"}
            unit="mm"
            delta={shmPoints?.vibration ? "+0.02" : "—"}
          />
          <MiniSignal
            title="位移监测"
            value={shmPoints?.displacement ? shmPoints.displacement.value.toFixed(4) : "—"}
            unit="m"
            delta={shmPoints?.displacement ? "+0.01" : "—"}
          />
          <div className="mini-card">
            <div className="mini-title">水位监测</div>
            <div className="mini-sub">实时数据</div>
            <div className="mini-value-row">
              <strong>{shmPoints?.water_level ? shmPoints.water_level.value.toFixed(1) : "—"}</strong>
              <span className="text-ok">m</span>
            </div>
            {shmData?.length ? (
              <ResponsiveContainer width="100%" height={72}>
                <BarChart data={shmData.filter(d => d.data_type === 'displacement').slice(0, 6)}>
                  <CartesianGrid stroke="rgba(148,163,184,0.16)" vertical={false} />
                  <XAxis dataKey="data_type" hide />
                  <YAxis hide />
                  <Bar dataKey="data_value" fill="#8db8ff" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : null}
          </div>
          <MiniSignal title="高风险事件" value={String(summary?.high_risk ?? 0)} unit="条" delta={`${summary?.high_risk ? "需处理" : "正常"}`} />
          <MiniSignal title="未读告警" value={String(unreadAlerts?.count ?? 0)} unit="条" delta={unreadAlerts?.count ? "待确认" : "无"} danger={!!unreadAlerts?.count} />
          <MiniSignal title="监测对象" value={String(summary?.total_objects ?? 0)} unit="个" delta="在线" />
        </div>
      </Panel>

      {/* ── Ship collision + Tunnel + Video ─────────────────────── */}
      <div className="dashboard-row lower-row">
        <Panel title="船撞融合预警">
          <div className="mega-card">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="mini-title">融合评分</div>
                <div className="mt-2 text-3xl font-semibold text-white">
                  {latestFusion ? `${latestFusion.score}` : "—"}
                </div>
              </div>
              <StatusPill tone={latestFusion?.risk_level === "high" ? "danger" : latestFusion?.risk_level === "medium" ? "warning" : "neutral"}>
                {latestFusion?.risk_level === "high" ? "高风险" : latestFusion?.risk_level === "medium" ? "中风险" : "无数据"}
              </StatusPill>
            </div>
            <div className="bridge-sketch mt-4">
              <div className="bridge-tower left" />
              <div className="bridge-tower right" />
            </div>
            <div className="ship-info">
              <span>{latestFusion?.rule_desc?.slice(0, 30) ?? "暂无融合分析数据"}</span>
            </div>
          </div>
        </Panel>

        <Panel title="隧道监测 / 南山隧道">
          <div className="gauge-row">
            <Gauge label="CO 指数" value={tunnelLatest?.co ? Math.round(tunnelLatest.co).toString() : "—"} unit="ppm" progress={tunnelLatest?.co ? `${Math.min(100, Math.round(tunnelLatest.co * 1.5))}%` : "0%"} />
            <Gauge label="照度" value={tunnelLatest?.lux ? Math.round(tunnelLatest.lux).toString() : "—"} unit="lux" progress={tunnelLatest?.lux ? `${Math.round(tunnelLatest.lux / 2.5)}%` : "0%"} />
            <Gauge label="交通流量" value={tunnelLatest?.traffic ? Math.round(tunnelLatest.traffic).toString() : "—"} unit="辆/h" progress={tunnelLatest?.traffic ? `${Math.round(tunnelLatest.traffic / 18)}%` : "0%"} />
            <Gauge label="告警" value={String(unreadAlerts?.count ?? 0)} unit="条" progress={unreadAlerts?.count ? "60%" : "0%"} />
          </div>
        </Panel>

        <Panel title="视频监控列表">
          <div className="video-grid">
            {videoList.length === 0 ? (
              <div className="col-span-2 py-8 text-center text-sm text-slate-500">暂无视频数据</div>
            ) : (
              videoList.slice(0, 4).map((v: { video_id: string; video_name?: string | null; scene_type?: string | null }) => (
                <button key={v.video_id} type="button" className="video-tile text-left">
                  <div className="video-thumb" />
                  <div className="video-meta">
                    <div className="font-medium text-white">{v.video_name || v.video_id}</div>
                    <div className="mt-3 flex items-center justify-between gap-2">
                      <span className="text-sm text-slate-400">{v.scene_type || "—"}</span>
                      <StatusPill tone="ok">就绪</StatusPill>
                    </div>
                  </div>
                </button>
              ))
            )}
          </div>
        </Panel>
      </div>
    </div>
  );
}

// ── Helper components ─────────────────────────────────────────────

function MiniSignal({ title, value, unit, delta, danger = false }: {
  title: string; value: string; unit: string; delta: string; danger?: boolean;
}) {
  return (
    <div className="mini-card">
      <div className="mini-title">{title}</div>
      <div className="mini-sub">{unit}</div>
      <div className="mini-value-row">
        <strong>{value}</strong>
        <span className={danger ? "text-danger" : "text-ok"}>{delta}</span>
      </div>
    </div>
  );
}

function Gauge({ label, value, unit, progress }: {
  label: string; value: string; unit: string; progress: string;
}) {
  return (
    <div className="gauge">
      <div className="mini-title">{label}</div>
      <div className="gauge-ring" style={{ "--progress": progress } as React.CSSProperties}>
        <span>{value}</span>
      </div>
      <div className="mt-3 text-center text-sm text-slate-300">{unit}</div>
    </div>
  );
}
