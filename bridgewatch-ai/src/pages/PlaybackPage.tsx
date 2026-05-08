import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { shipMonitoringSeries } from "../data/mockData";
import type { EventRecord } from "../types";
import { Panel } from "../components/Panel";
import { PlaybackFrame } from "../components/PlaybackFrame";
import { StatusPill } from "../components/StatusPill";

interface PlaybackPageProps {
  event: EventRecord;
  onSelectEvent: (eventId: string) => void;
  relatedEvents: EventRecord[];
}

export function PlaybackPage({ event, onSelectEvent, relatedEvents }: PlaybackPageProps) {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
        <Panel title="关键片段回放" eyebrow="Playback Deck">
          <PlaybackFrame event={event} />
          <div className="mt-4 rounded-[1.2rem] border border-slate-700 bg-slate-950/35 p-4">
            <div className="mb-2 flex items-center justify-between">
              <p className="panel-eyebrow">Timeline Markers</p>
              <span className="font-mono text-xs uppercase tracking-[0.18em] text-slate-400">{event.clipRange}</span>
            </div>
            <div className="relative mt-6 h-3 rounded-full bg-slate-800">
              <div className="absolute inset-y-0 left-[18%] right-[22%] rounded-full bg-[#d3914d]/65" />
              {relatedEvents.slice(0, 4).map((related, index) => (
                <button
                  key={related.id}
                  type="button"
                  onClick={() => onSelectEvent(related.id)}
                  className={`absolute top-1/2 h-4 w-4 -translate-y-1/2 rounded-full border-2 ${
                    related.id === event.id ? "border-white bg-white" : "border-[#d3914d] bg-slate-900"
                  }`}
                  style={{ left: `${12 + index * 22}%` }}
                  aria-label={related.title}
                />
              ))}
            </div>
          </div>
        </Panel>

        <Panel title="复盘参数" eyebrow="Inspection Sheet">
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <StatusPill tone={event.riskLevel === "高" ? "danger" : event.riskLevel === "中" ? "warning" : "low"}>
                {event.riskLevel}风险
              </StatusPill>
              <StatusPill tone="neutral">{event.scene}</StatusPill>
              <StatusPill tone="info">置信度 {event.confidence}%</StatusPill>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              {[
                ["监测对象", event.objectName],
                ["镜头编号", event.camera],
                ["事件时间", event.time],
                ["片段窗口", event.clipRange]
              ].map(([label, value]) => (
                <div key={label} className="rounded-[1rem] border border-slate-700 bg-slate-950/35 p-4">
                  <div className="panel-eyebrow">{label}</div>
                  <div className="mt-2 font-medium text-white">{value}</div>
                </div>
              ))}
            </div>
            <div className="rounded-[1.1rem] border border-slate-700 bg-slate-900/40 p-4">
              <p className="panel-eyebrow">Interpretation</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">{event.description}</p>
            </div>
          </div>
        </Panel>
      </div>

      <Panel title="关联传感曲线" eyebrow="Cross Check">
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={shipMonitoringSeries}>
              <CartesianGrid stroke="rgba(148,163,184,0.14)" vertical={false} />
              <XAxis dataKey="label" tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <YAxis tickLine={false} axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} />
              <Tooltip
                contentStyle={{
                  background: "#0f1724",
                  borderRadius: "16px",
                  border: "1px solid rgba(148,163,184,0.18)",
                  color: "#e2e8f0"
                }}
              />
              <Line type="monotone" dataKey="impact" stroke="#d3914d" strokeWidth={2.5} dot={false} />
              <Line type="monotone" dataKey="strain" stroke="#7cb3ff" strokeWidth={2.5} dot={false} />
              <Line type="monotone" dataKey="clearance" stroke="#6cd5b7" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Panel>
    </div>
  );
}
