import type { EventRecord } from "../types";
import { StatusPill } from "./StatusPill";

interface EventTableProps {
  events: EventRecord[];
  selectedEventId: string;
  onSelect: (eventId: string) => void;
  onPlayback: (eventId: string) => void;
}

function riskTone(level: EventRecord["riskLevel"]) {
  if (level === "高") return "danger";
  if (level === "中") return "warning";
  return "low";
}

export function EventTable({
  events: rows,
  selectedEventId,
  onSelect,
  onPlayback
}: EventTableProps) {
  return (
    <div className="overflow-hidden rounded-[1.3rem] border border-slate-700/50">
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead>
            <tr className="border-b border-slate-700/50 bg-slate-900/35 text-left font-mono text-[0.72rem] uppercase tracking-[0.18em] text-slate-400">
              <th className="px-4 py-3">时间</th>
              <th className="px-4 py-3">对象</th>
              <th className="px-4 py-3">事件</th>
              <th className="px-4 py-3">风险</th>
              <th className="px-4 py-3">场景</th>
              <th className="px-4 py-3">状态</th>
              <th className="px-4 py-3">操作</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((event) => {
              const active = event.id === selectedEventId;

              return (
                <tr
                  key={event.id}
                  className={`border-b border-slate-800/70 transition ${
                    active ? "bg-slate-100/8 text-white" : "bg-transparent hover:bg-white/3"
                  }`}
                >
                  <td className="px-4 py-3 font-mono text-xs">{event.time}</td>
                  <td className="px-4 py-3">
                    <div className="font-medium">{event.objectName}</div>
                    <div className={`text-xs ${active ? "text-slate-300" : "text-slate-400"}`}>{event.objectType}</div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="font-medium">{event.title}</div>
                    <div className={`text-xs ${active ? "text-slate-300" : "text-slate-400"}`}>置信度 {event.confidence}%</div>
                  </td>
                  <td className="px-4 py-3">
                    <StatusPill tone={riskTone(event.riskLevel)}>{event.riskLevel}风险</StatusPill>
                  </td>
                  <td className="px-4 py-3 text-sm">{event.scene}</td>
                  <td className="px-4 py-3 text-sm">{event.status}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => onSelect(event.id)}
                        className={`rounded-full border px-3 py-1.5 text-xs transition ${
                          active
                            ? "border-white/20 bg-white/10 text-white"
                            : "border-slate-700 bg-slate-900/45 text-slate-200 hover:border-slate-500"
                        }`}
                      >
                        详情
                      </button>
                      <button
                        type="button"
                        onClick={() => onPlayback(event.id)}
                        className={`rounded-full border px-3 py-1.5 text-xs transition ${
                          active
                            ? "border-white/20 bg-white/10 text-white"
                            : "border-slate-700 bg-slate-900/45 text-slate-200 hover:border-slate-500"
                        }`}
                      >
                        回放
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
