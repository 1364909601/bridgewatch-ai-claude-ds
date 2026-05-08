import {
  Activity,
  BarChart3,
  Bell,
  Cable,
  Database,
  FileText,
  Map,
  Settings,
  Ship,
  Video
} from "lucide-react";
import type { NavItem, PageId } from "../types";

interface PageNavProps {
  items: NavItem[];
  activeId: PageId;
  onNavigate: (id: PageId) => void;
  compact?: boolean;
}

const icons: Record<PageId, typeof Activity> = {
  overview: BarChart3,
  events: Bell,
  playback: Video,
  ordinary: Activity,
  ship: Ship,
  tunnel: Cable,
  ops: Settings
};

export function PageNav({ items, activeId, onNavigate, compact = false }: PageNavProps) {
  return (
    <nav className={compact ? "mobile-nav" : "side-nav"}>
      {items.map((item) => {
        const active = item.id === activeId;
        const Icon = icons[item.id] ?? Map;

        return (
          <button
            key={item.id}
            type="button"
            onClick={() => onNavigate(item.id)}
            className={`nav-button ${active ? "is-active" : ""}`}
            title={item.eyebrow}
          >
            <Icon size={16} strokeWidth={1.8} />
            <span>{item.label}</span>
          </button>
        );
      })}
      {!compact ? (
        <div className="mt-3 border-t border-slate-700/60 pt-3">
          <button type="button" className="nav-button">
            <Database size={16} strokeWidth={1.8} />
            <span>报告中心</span>
          </button>
          <button type="button" className="nav-button">
            <FileText size={16} strokeWidth={1.8} />
            <span>系统设置</span>
          </button>
        </div>
      ) : null}
    </nav>
  );
}
