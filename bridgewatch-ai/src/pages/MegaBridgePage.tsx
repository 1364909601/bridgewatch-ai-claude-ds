import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { fusionFactors, shipMonitoringSeries, shipTrack } from "../data/mockData";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";

function ShipTrackFigure() {
  const points = shipTrack.map((point) => `${point.x},${point.y}`).join(" ");

  return (
    <svg viewBox="0 0 280 180" className="h-full w-full rounded-[1.2rem] bg-[linear-gradient(135deg,#12243b,#0c1728)]">
      <rect x="0" y="0" width="280" height="180" fill="transparent" />
      <path d="M0 120C48 104 78 142 120 120C165 96 208 58 280 80V180H0Z" fill="rgba(108,213,183,0.12)" />
      <line x1="140" y1="12" x2="140" y2="168" stroke="rgba(255,255,255,0.32)" strokeWidth="10" />
      <line x1="164" y1="12" x2="164" y2="168" stroke="rgba(255,255,255,0.18)" strokeWidth="10" />
      <polyline points={points} fill="none" stroke="#D3914D" strokeWidth="4" strokeDasharray="6 6" />
      {shipTrack.map((point, index) => (
        <g key={`${point.label}-${index}`}>
          <circle cx={point.x} cy={point.y} r={index === shipTrack.length - 1 ? 8 : 5} fill="#F8FAFC" />
          <text x={point.x + 8} y={point.y - 8} fontSize="10" fill="#E2E8F0">
            {point.label}
          </text>
        </g>
      ))}
      <text x="124" y="96" fontSize="11" fill="#E2E8F0">
        PIER-01
      </text>
      <text x="148" y="96" fontSize="11" fill="#E2E8F0">
        PIER-02
      </text>
    </svg>
  );
}

export function MegaBridgePage() {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 xl:grid-cols-[1.05fr_0.95fr]">
        <Panel title="船迹与桥区关系" eyebrow="Ship Track Fusion">
          <div className="grid gap-4 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="h-[280px]">
              <ShipTrackFigure />
            </div>
            <div className="space-y-3">
              {[
                ["一级保护圈", "36m", "danger"],
                ["应变抬升", "+18%", "warning"],
                ["偏航修正", "2 次", "neutral"]
              ].map(([label, value, tone]) => (
                <div key={label} className="rounded-[1.1rem] border border-slate-700 bg-slate-950/35 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="panel-eyebrow">{label}</div>
                      <div className="mt-2 font-mono text-3xl text-white">{value}</div>
                    </div>
                    <StatusPill tone={tone as "danger" | "warning" | "neutral"}>{label}</StatusPill>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Panel>

        <Panel title="融合构成" eyebrow="Risk Composition">
          <div className="space-y-3">
            {fusionFactors.map((factor) => (
              <div key={factor.label} className="rounded-[1.2rem] border border-slate-700 bg-slate-950/35 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="font-medium text-white">{factor.label}</div>
                    <div className="mt-1 text-sm text-slate-400">{factor.note}</div>
                  </div>
                  <div className="font-mono text-2xl text-white">{factor.score}</div>
                </div>
                <div className="mt-3 h-2 rounded-full bg-slate-800">
                  <div className="h-2 rounded-full bg-[#d3914d]" style={{ width: `${factor.score}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <Panel title="桥区监测曲线" eyebrow="SHM Overlay">
        <div className="h-[320px]">
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
