import { useDeferredValue, useState } from "react";
import type { EventRecord } from "../types";
import { EventTable } from "../components/EventTable";
import { Panel } from "../components/Panel";
import { PlaybackFrame } from "../components/PlaybackFrame";
import { StatusPill } from "../components/StatusPill";

interface EventCenterPageProps {
  events: EventRecord[];
  selectedEvent: EventRecord;
  onSelectEvent: (eventId: string) => void;
  onOpenPlayback: (eventId: string) => void;
}

export function EventCenterPage({
  events,
  selectedEvent,
  onSelectEvent,
  onOpenPlayback
}: EventCenterPageProps) {
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState<"全部" | EventRecord["riskLevel"]>("全部");
  const deferredSearch = useDeferredValue(search);

  const filteredEvents = events.filter((event) => {
    const hitSearch =
      deferredSearch.trim() === "" ||
      `${event.objectName} ${event.title} ${event.type}`.toLowerCase().includes(deferredSearch.toLowerCase());
    const hitRisk = riskFilter === "全部" || event.riskLevel === riskFilter;
    return hitSearch && hitRisk;
  });

  return (
    <div className="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
      <div className="space-y-4">
        <Panel title="事件检索台" eyebrow="Event Ledger">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div className="grid flex-1 gap-3 md:grid-cols-[1fr_auto]">
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="搜索对象、事件标题或事件类型"
                className="rounded-full border border-slate-700 bg-slate-950/50 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-slate-400"
              />
              <div className="flex gap-2">
                {(["全部", "高", "中", "低"] as const).map((risk) => (
                  <button
                    key={risk}
                    type="button"
                    onClick={() => setRiskFilter(risk)}
                    className={`rounded-full border px-4 py-2 text-sm transition ${
                      risk === riskFilter
                        ? "border-slate-300 bg-slate-100 text-slate-950"
                        : "border-slate-700 bg-slate-900/60 text-slate-200 hover:border-slate-500"
                    }`}
                  >
                    {risk}
                  </button>
                ))}
              </div>
            </div>
            <div className="font-mono text-xs uppercase tracking-[0.2em] text-slate-500">{filteredEvents.length} entries</div>
          </div>
        </Panel>

        <Panel title="事件列表" eyebrow="Review Queue">
          <EventTable
            events={filteredEvents}
            selectedEventId={selectedEvent.id}
            onSelect={onSelectEvent}
            onPlayback={onOpenPlayback}
          />
        </Panel>
      </div>

      <div className="space-y-4">
        <Panel title="当前事件预览" eyebrow="Focused Incident">
          <PlaybackFrame event={selectedEvent} />
        </Panel>

        <Panel title={selectedEvent.title} eyebrow={selectedEvent.objectName}>
          <div className="space-y-5">
            <div className="flex flex-wrap gap-2">
              <StatusPill tone={selectedEvent.riskLevel === "高" ? "danger" : selectedEvent.riskLevel === "中" ? "warning" : "low"}>
                {selectedEvent.riskLevel}风险
              </StatusPill>
              <StatusPill tone="neutral">{selectedEvent.scene}</StatusPill>
              <StatusPill tone={selectedEvent.status === "已确认" ? "ok" : "neutral"}>{selectedEvent.status}</StatusPill>
            </div>
            <dl className="grid gap-4 md:grid-cols-2">
              <div className="rounded-[1.1rem] border border-slate-700 bg-slate-950/35 p-4">
                <dt className="panel-eyebrow">Sensor Trigger</dt>
                <dd className="mt-2 text-sm leading-6 text-slate-300">{selectedEvent.sensorSignal}</dd>
              </div>
              <div className="rounded-[1.1rem] border border-slate-700 bg-slate-950/35 p-4">
                <dt className="panel-eyebrow">Clip Window</dt>
                <dd className="mt-2 font-mono text-sm text-slate-300">{selectedEvent.clipRange}</dd>
              </div>
            </dl>
            <div className="rounded-[1.2rem] border border-slate-700 bg-slate-900/40 p-4">
              <p className="panel-eyebrow">Analyst Notes</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">{selectedEvent.description}</p>
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => onOpenPlayback(selectedEvent.id)}
                className="rounded-full border border-slate-200 bg-slate-100 px-4 py-2 text-sm text-slate-950 transition hover:bg-white"
              >
                跳转回放
              </button>
              <button
                type="button"
                className="rounded-full border border-slate-700 bg-slate-900/60 px-4 py-2 text-sm text-slate-200 transition hover:border-slate-500"
              >
                标记已复核
              </button>
            </div>
          </div>
        </Panel>
      </div>
    </div>
  );
}
