import type { ReactNode } from "react";

interface StatusPillProps {
  children: ReactNode;
  tone?: "danger" | "warning" | "low" | "info" | "ok" | "neutral";
}

export function StatusPill({ children, tone = "neutral" }: StatusPillProps) {
  return <span className={`status-pill status-${tone}`}>{children}</span>;
}
