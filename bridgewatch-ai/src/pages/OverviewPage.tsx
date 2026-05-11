import { Maximize2, Minus, Plus } from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import {
  events,
  loadSeries,
  systemStats,
  trendSeries,
  videoFeeds
} from "../data/mockData";
import type { DashboardMetric, PageId } from "../types";
import { MetricCard } from "../components/MetricCard";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";
import { useDashboardSummary } from "../hooks/use-dashboard";

interface OverviewPageProps {
  onFocusEvent: (eventId: string, targetPage?: PageId) => void;
}

export function OverviewPage({ onFocusEvent }: OverviewPageProps) {
  const { data: summary, isLoading } = useDashboardSummary();

  const metrics: DashboardMetric[] = isLoading
    ? [
        { id: "high", label: "高风险事件", value: "—", hint: "加载中...", tone: "danger" },
        { id: "medium", label: "中风险事件", value: "—", hint: "加载中...", tone: "warning" },
        { id: "low", label: "低风险事件", value: "—", hint: "加载中...", tone: "low" },
        { id: "monitored", label: "监测对象", value: "—", hint: "加载中...", tone: "info" },
      ]
    : [
        { id: "high", label: "高风险事件", value: String(summary?.high_risk ?? 0), hint: "需要立即复核", tone: "danger" },
        { id: "medium", label: "中风险事件", value: String(summary?.medium_risk ?? 0), hint: "需要持续关注", tone: "warning" },
        { id: "low", label: "低风险事件", value: String(summary?.low_risk ?? 0), hint: "维持自动巡检", tone: "low" },
        { id: "monitored", label: "监测对象", value: String(summary?.total_objects ?? 0), hint: "桥梁与隧道总数", tone: "info" },
      ];

  return (
    <div className="dashboard-stack">
      <div className="risk-grid">
        {metrics.map((metric) => (
          <MetricCard key={metric.id} metric={metric} />
        ))}
      </div>

      <div className="dashboard-row main-row">
        <Panel
          title="监测对象分布"
          action={
            <div className="flex gap-2">
              <StatusPill tone="neutral">全部</StatusPill>
              <StatusPill tone="info">桥梁 18</StatusPill>
              <StatusPill tone="low">隧道 10</StatusPill>
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
              <button type="button" title="全屏">
                <Maximize2 size={16} />
              </button>
              <button type="button" title="放大">
                <Plus size={16} />
              </button>
              <button type="button" title="缩小">
                <Minus size={16} />
              </button>
            </div>
          </div>
        </Panel>

        <Panel title="系统状态总览">
          <div className="system-list">
            {systemStats.map((stat) => (
              <div key={stat.label} className="system-row">
                <div className="flex items-center gap-3">
                  <span className="green-dot" />
                  <div>
                    <strong>{stat.label}</strong>
                    <div className="mt-1 text-sm text-slate-400">{stat.status}</div>
                  </div>
                </div>
                <div className="text-right">
                  <strong>{stat.value}</strong>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <Panel title="结构健康监测 / 南京长江大桥 #B-001" action={<span className="timestamp">14:32:18</span>}>
        <div className="shm-grid">
          <MiniSignal title="振动监测" value="0.256" unit="m/s²" delta="+12.5%" />
          <MiniSignal title="应变监测" value="156.8" unit="με" delta="+8.3%" danger />
          <div className="mini-card">
            <div className="mini-title">荷载分布</div>
            <div className="mini-sub">按桥位实时更新</div>
            <ResponsiveContainer width="100%" height={132}>
              <BarChart data={loadSeries}>
                <XAxis dataKey="zone" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 11 }} />
                <YAxis hide />
                <Tooltip />
                <Bar dataKey="load" fill="#8db8ff" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <MiniSignal title="位移监测" value="2.34" unit="mm" delta="+3.2%" />
          <MiniSignal title="温度监测" value="23.6" unit="℃" delta="0.0%" />
          <MiniSignal title="异常指数" value="0.82" unit="score" delta="+5.4%" danger />
        </div>
      </Panel>

      <div className="dashboard-row lower-row">
        <Panel title="船撞融合预警原型">
          <div className="mega-card">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="mini-title">通航净空</div>
                <div className="mt-2 text-3xl font-semibold text-white">32.5m</div>
              </div>
              <StatusPill tone="warning">接近预警</StatusPill>
            </div>
            <div className="bridge-sketch mt-4">
              <div className="bridge-tower left" />
              <div className="bridge-tower right" />
            </div>
            <div className="ship-info">
              <span>最近目标：长明货轮</span>
              <span>航速 12.5 kn</span>
            </div>
          </div>
        </Panel>

        <Panel title="隧道监测专题 / 海沧隧道 #T-009">
          <div className="gauge-row">
            <Gauge label="空气质量" value="42" unit="AQI" progress="42%" />
            <Gauge label="能见度" value="2.8" unit="km" progress="58%" />
            <Gauge label="照度" value="156" unit="lux" progress="66%" />
            <Gauge label="交通流量" value="1256" unit="辆/h" progress="72%" />
          </div>
          <div className="incident-row mt-3 flex items-center justify-between text-sm text-slate-300">
            <span>火灾报警 0</span>
            <span>设备故障 1</span>
            <span>交通事故 0</span>
            <span>异常停留 1</span>
          </div>
        </Panel>

        <Panel title="视频监控实时卡片">
          <div className="video-grid">
            {videoFeeds.map((feed, index) => (
              <button
                key={feed.name}
                type="button"
                className="video-tile text-left"
                onClick={() => onFocusEvent(events[index]?.id ?? events[0].id, "playback")}
              >
                <div className="video-thumb" />
                <div className="video-meta">
                  <div className="font-medium text-white">{feed.name}</div>
                  <div className="mt-3 flex items-center justify-between gap-2">
                    <span className="text-sm text-slate-400">无人机巡检流</span>
                    <StatusPill tone={feed.tone}>{feed.state}</StatusPill>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}

function MiniSignal({
  title,
  value,
  unit,
  delta,
  danger = false
}: {
  title: string;
  value: string;
  unit: string;
  delta: string;
  danger?: boolean;
}) {
  return (
    <div className="mini-card">
      <div className="mini-title">{title}</div>
      <div className="mini-sub">{unit}</div>
      <div className="mini-value-row">
        <strong>{value}</strong>
        <span className={danger ? "text-danger" : "text-ok"}>{delta}</span>
      </div>
      <ResponsiveContainer width="100%" height={72}>
        <AreaChart data={trendSeries}>
          <defs>
            <linearGradient id={`line-${title}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#7cb3ff" stopOpacity={0.26} />
              <stop offset="100%" stopColor="#7cb3ff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="rgba(148,163,184,0.16)" vertical={false} />
          <Area type="monotone" dataKey="strainIndex" stroke="#7cb3ff" fill={`url(#line-${title})`} strokeWidth={1.6} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

function Gauge({
  label,
  value,
  unit,
  progress
}: {
  label: string;
  value: string;
  unit: string;
  progress: string;
}) {
  return (
    <div className="gauge">
      <div className="mini-title">{label}</div>
      <div className="gauge-ring" style={{ ["--progress" as string]: progress }}>
        <span>{value}</span>
      </div>
      <div className="mt-3 text-center text-sm text-slate-300">{unit}</div>
    </div>
  );
}
