import { AlertTriangle, CircleArrowDown, Info, ShieldCheck } from "lucide-react";
import type { DashboardMetric } from "../types";

interface MetricCardProps {
  metric: DashboardMetric;
}

const iconMap = {
  danger: AlertTriangle,
  warning: AlertTriangle,
  low: AlertTriangle,
  info: CircleArrowDown,
  ok: ShieldCheck
};

export function MetricCard({ metric }: MetricCardProps) {
  const Icon = iconMap[metric.tone] ?? Info;

  return (
    <article className="risk-card">
      <div className={`risk-icon risk-${metric.tone}`}>
        <Icon size={28} strokeWidth={1.8} />
      </div>
      <div className="min-w-0">
        <div className={`risk-value risk-text-${metric.tone}`}>{metric.value}</div>
        <div className="risk-label">{metric.label}</div>
      </div>
      <div className="ml-auto text-right text-[12px] text-slate-500">{metric.hint}</div>
    </article>
  );
}
