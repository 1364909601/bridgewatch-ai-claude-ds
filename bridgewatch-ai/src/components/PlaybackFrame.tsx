import type { EventRecord } from "../types";

interface PlaybackFrameProps {
  event: EventRecord;
}

export function PlaybackFrame({ event }: PlaybackFrameProps) {
  return (
    <div className="relative overflow-hidden rounded-[1.5rem] border border-ink/10 bg-[linear-gradient(135deg,rgba(26,26,23,0.9),rgba(48,55,49,0.82))] p-4 shadow-[0_24px_60px_rgba(26,26,23,0.16)]">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:18px_18px]" />
      <div className="relative aspect-video overflow-hidden rounded-[1.2rem] border border-white/10 bg-[radial-gradient(circle_at_20%_20%,rgba(194,125,60,0.28),transparent_28%),linear-gradient(135deg,rgba(255,255,255,0.08),rgba(255,255,255,0.02))]">
        <div className="absolute inset-x-0 top-[56%] h-[2px] bg-white/20" />
        <div className="absolute left-[10%] top-[38%] h-[14%] w-[72%] rounded-full border border-white/12" />
        {event.overlays.map((overlay) => (
          <div
            key={overlay.id}
            className="absolute border border-brass bg-brass/12 shadow-[0_0_0_1px_rgba(194,125,60,0.22)]"
            style={{
              left: `${overlay.left}%`,
              top: `${overlay.top}%`,
              width: `${overlay.width}%`,
              height: `${overlay.height}%`
            }}
          >
            <span className="absolute -top-6 left-0 rounded-full bg-brass px-2 py-1 font-mono text-[0.65rem] uppercase tracking-[0.16em] text-paper">
              {overlay.label}
            </span>
          </div>
        ))}
      </div>
      <div className="relative mt-4 flex flex-wrap items-center justify-between gap-3 font-mono text-[0.7rem] uppercase tracking-[0.18em] text-paper/72">
        <span>{event.camera}</span>
        <span>{event.clipRange}</span>
        <span>{event.objectName}</span>
      </div>
    </div>
  );
}
