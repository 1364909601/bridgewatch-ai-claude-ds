import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { events, tunnelSeries } from "../data/mockData";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";

export function TunnelPage() {
  const tunnelEvents = events.filter((event) => event.objectType === "隧道");

  return (
    <div className="space-y-4">
      <div className="grid gap-4 xl:grid-cols-[1.1fr_0.9fr]">
        <Panel title="环境与交通走势" eyebrow="Tunnel Signals">
          <div className="h-[310px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={tunnelSeries}>
                <defs>
                  <linearGradient id="coGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#D3914D" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="#D3914D" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
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
                <Area type="monotone" dataKey="coIndex" stroke="#D3914D" fill="url(#coGradient)" strokeWidth={2.5} />
                <Line type="monotone" dataKey="lux" stroke="#7cb3ff" strokeWidth={2.5} dot={false} />
                <Line type="monotone" dataKey="traffic" stroke="#6cd5b7" strokeWidth={2.5} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="当班隧道异常" eyebrow="Alert Capsules">
          <div className="space-y-3">
            {tunnelEvents.map((event) => (
              <div key={event.id} className="rounded-[1.2rem] border border-slate-700 bg-slate-950/35 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="font-medium text-white">{event.title}</div>
                    <div className="mt-1 text-sm text-slate-400">{event.time}</div>
                  </div>
                  <StatusPill tone={event.riskLevel === "高" ? "danger" : event.riskLevel === "中" ? "warning" : "low"}>
                    {event.riskLevel}
                  </StatusPill>
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-300">{event.description}</p>
                <div className="mt-3 font-mono text-xs uppercase tracking-[0.18em] text-slate-500">{event.sensorSignal}</div>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}
