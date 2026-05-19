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
  ops: Settings,
  reports: Database,
  settings: FileText,
  audit: Activity,
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
    </nav>
  );
}
