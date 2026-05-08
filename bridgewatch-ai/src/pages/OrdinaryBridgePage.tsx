import {
  Bar,
  BarChart,
  CartesianGrid,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { events, readinessRadar, sceneAssessment } from "../data/mockData";
import type { PageId } from "../types";
import { MetricCard } from "../components/MetricCard";
import { Panel } from "../components/Panel";

interface OrdinaryBridgePageProps {
  onFocusEvent: (eventId: string, targetPage?: PageId) => void;
}

export function OrdinaryBridgePage({ onFocusEvent }: OrdinaryBridgePageProps) {
  const bridgeEvents = events.filter((event) => event.objectType === "普通桥梁");
  const cards = [
    { id: "collapse", label: "坍塌识别", value: "02", hint: "高危样例", tone: "danger" as const },
    { id: "deform", label: "桥面变形", value: "06", hint: "夜雨弱项", tone: "warning" as const },
    { id: "traffic", label: "车辆积压", value: "11", hint: "成熟度最高", tone: "ok" as const },
    { id: "fire", label: "桥面火灾", value: "04", hint: "多信号联动", tone: "danger" as const }
  ];

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((metric) => (
          <MetricCard key={metric.id} metric={metric} />
        ))}
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
        <Panel title="分场景识别表现" eyebrow="Scene Benchmark">
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sceneAssessment} barGap={10}>
                <CartesianGrid stroke="rgba(148,163,184,0.14)" vertical={false} />
                <XAxis dataKey="metric" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: "#0f1724",
                    borderRadius: "16px",
                    border: "1px solid rgba(148,163,184,0.18)",
                    color: "#e2e8f0"
                  }}
                />
                <Bar dataKey="day" fill="#7cb3ff" radius={[10, 10, 0, 0]} />
                <Bar dataKey="night" fill="#d3914d" radius={[10, 10, 0, 0]} />
                <Bar dataKey="fog" fill="#6cd5b7" radius={[10, 10, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="模型就绪雷达" eyebrow="Readiness Profile">
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={readinessRadar}>
                <PolarGrid stroke="rgba(148,163,184,0.24)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
                <Radar dataKey="score" stroke="#d3914d" fill="#d3914d" fillOpacity={0.25} />
                <Tooltip
                  contentStyle={{
                    background: "#0f1724",
                    borderRadius: "16px",
                    border: "1px solid rgba(148,163,184,0.18)",
                    color: "#e2e8f0"
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>

      <Panel title="典型案例卡" eyebrow="Showcase Cases">
        <div className="grid gap-4 lg:grid-cols-3">
          {bridgeEvents.map((event) => (
            <button
              key={event.id}
              type="button"
              onClick={() => onFocusEvent(event.id, "playback")}
              className="overflow-hidden rounded-[1.35rem] border border-slate-700 bg-slate-950/35 text-left transition hover:border-slate-500 hover:bg-slate-900/55"
            >
              <div className="h-34 bg-[linear-gradient(135deg,rgba(10,22,37,0.96),rgba(36,63,90,0.86))]" />
              <div className="space-y-3 p-4">
                <div className="panel-eyebrow">{event.type}</div>
                <h4 className="font-medium text-white">{event.title}</h4>
                <p className="text-sm leading-6 text-slate-300">{event.description}</p>
              </div>
            </button>
          ))}
        </div>
      </Panel>
    </div>
  );
}
