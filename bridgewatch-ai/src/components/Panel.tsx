import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function Panel({ title, eyebrow, action, children, className = "" }: PanelProps) {
  return (
    <section className={`panel ${className}`}>
      <header className="panel-header">
        <div>
          <h3 className="panel-title">{title}</h3>
          {eyebrow ? <p className="panel-eyebrow">{eyebrow}</p> : null}
        </div>
        {action ? <div className="panel-action">{action}</div> : null}
      </header>
      <div>{children}</div>
    </section>
  );
}
