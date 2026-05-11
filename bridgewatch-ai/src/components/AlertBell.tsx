import { Bell, Check, Loader2 } from "lucide-react";
import { useState } from "react";
import { useAlerts, useAcknowledgeAlert, useUnreadAlertCount } from "../hooks/use-alerts";
import type { AlertItem } from "../lib/api";
import { StatusPill } from "./StatusPill";

function severityColor(severity: string) {
  switch (severity) {
    case "critical": return "danger";
    case "warning": return "warning";
    default: return "info";
  }
}

function AlertRow({ alert, onAck }: { alert: AlertItem; onAck: (id: string) => void }) {
  const [acknowledging, setAcknowledging] = useState(false);

  return (
    <div className={`flex items-start gap-3 border-b border-slate-700/40 px-4 py-3 text-left transition hover:bg-white/3 ${
      alert.status === "unread" ? "bg-slate-800/40" : ""
    }`}>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <StatusPill tone={severityColor(alert.severity)}>
            {alert.severity === "critical" ? "紧急" : alert.severity === "warning" ? "警告" : "通知"}
          </StatusPill>
          <span className="text-xs text-slate-400">{alert.alert_type}</span>
        </div>
        <div className="mt-1 text-sm font-medium text-white">{alert.title}</div>
        {alert.message && (
          <div className="mt-0.5 text-xs text-slate-400 line-clamp-2">{alert.message}</div>
        )}
        <div className="mt-1 text-[0.65rem] text-slate-500">
          {alert.created_time ? new Date(alert.created_time).toLocaleString("zh-CN") : ""}
        </div>
      </div>
      {alert.status !== "acknowledged" && (
        <button
          type="button"
          disabled={acknowledging}
          onClick={() => {
            setAcknowledging(true);
            onAck(alert.alert_id);
          }}
          className="mt-1 shrink-0 rounded-full border border-slate-600 bg-slate-800/60 p-1.5 text-slate-300 transition hover:border-slate-400 hover:text-white disabled:opacity-50"
          title="确认"
        >
          {acknowledging ? <Loader2 size={14} className="animate-spin" /> : <Check size={14} />}
        </button>
      )}
    </div>
  );
}

export function AlertBell() {
  const [open, setOpen] = useState(false);
  const { data: unreadData } = useUnreadAlertCount();
  const { data: alertsData } = useAlerts({ page_size: 10 });
  const acknowledgeMutation = useAcknowledgeAlert();

  const unreadCount = unreadData?.count ?? 0;
  const alerts = alertsData?.list ?? [];

  const handleAcknowledge = (alertId: string) => {
    acknowledgeMutation.mutate(alertId, {
      onSettled: () => {
        // Refresh will happen via query invalidation
      },
    });
  };

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="icon-button relative"
        title="告警通知"
      >
        <Bell size={16} />
        {unreadCount > 0 && (
          <span className="absolute -right-1 -top-1 flex min-w-[18px] items-center justify-center rounded-full bg-danger px-1 text-[0.6rem] font-bold text-white">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <>
          {/* Backdrop to close on click outside */}
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />

          {/* Dropdown panel */}
          <div className="absolute right-0 top-full z-50 mt-2 w-[380px] overflow-hidden rounded-[1.2rem] border border-slate-700/60 bg-slate-900 shadow-[0_16px_48px_rgba(0,0,0,0.4)]">
            <div className="flex items-center justify-between border-b border-slate-700/40 px-4 py-3">
              <h3 className="text-sm font-semibold text-white">告警通知</h3>
              <span className="text-xs text-slate-400">
                {unreadCount > 0 ? `${unreadCount} 条未读` : "全部已读"}
              </span>
            </div>

            <div className="max-h-[360px] overflow-y-auto">
              {alerts.length === 0 ? (
                <div className="flex items-center justify-center py-10 text-sm text-slate-500">
                  暂无告警
                </div>
              ) : (
                alerts.map((alert) => (
                  <AlertRow key={alert.alert_id} alert={alert} onAck={handleAcknowledge} />
                ))
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
