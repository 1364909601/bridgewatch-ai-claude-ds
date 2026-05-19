import { useState } from "react";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";
import { useAuditLogs } from "../hooks/use-audit";

const LEVEL_COLORS: Record<string, "danger" | "warning" | "info" | "neutral"> = {
  error: "danger",
  warn: "warning",
  info: "info",
};

const TYPE_LABELS: Record<string, string> = {
  login: "登录认证",
  event_review: "事件复核",
  user_mgmt: "用户管理",
  task: "推理任务",
  alert: "告警通知",
  system: "系统",
};

export function AuditLogPage() {
  const [typeFilter, setTypeFilter] = useState<string>("");
  const { data, isLoading } = useAuditLogs({ page_size: 100, log_type: typeFilter || undefined });
  const logs = data?.list ?? [];

  return (
    <div className="space-y-4">
      <Panel title="审计日志" eyebrow="Audit Trail">
        {/* Filter */}
        <div className="mb-4 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setTypeFilter("")}
            className={`rounded-full border px-3 py-1.5 text-xs transition ${
              !typeFilter ? "border-slate-300 bg-slate-100 text-slate-950" : "border-slate-700 bg-slate-900/60 text-slate-200 hover:border-slate-500"
            }`}
          >
            全部
          </button>
          {Object.entries(TYPE_LABELS).map(([key, label]) => (
            <button
              key={key}
              type="button"
              onClick={() => setTypeFilter(key)}
              className={`rounded-full border px-3 py-1.5 text-xs transition ${
                typeFilter === key ? "border-slate-300 bg-slate-100 text-slate-950" : "border-slate-700 bg-slate-900/60 text-slate-200 hover:border-slate-500"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Table */}
        {isLoading ? (
          <div className="py-10 text-center text-sm text-slate-500">加载中...</div>
        ) : logs.length === 0 ? (
          <div className="py-10 text-center text-sm text-slate-500">暂无审计日志</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse">
              <thead>
                <tr className="border-b border-slate-700/50 bg-slate-900/35 text-left font-mono text-[0.7rem] uppercase tracking-[0.16em] text-slate-400">
                  <th className="px-3 py-2.5">时间</th>
                  <th className="px-3 py-2.5">类型</th>
                  <th className="px-3 py-2.5">级别</th>
                  <th className="px-3 py-2.5">操作人</th>
                  <th className="px-3 py-2.5">内容</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log: { log_id: number; log_type: string; log_level: string; operator_name?: string; log_content?: string; created_time?: string }) => (
                  <tr key={log.log_id} className="border-b border-slate-800/60 text-sm transition hover:bg-white/3">
                    <td className="whitespace-nowrap px-3 py-2.5 font-mono text-xs text-slate-400">
                      {log.created_time ? new Date(log.created_time).toLocaleString("zh-CN") : "—"}
                    </td>
                    <td className="px-3 py-2.5 text-slate-300">
                      {TYPE_LABELS[log.log_type] || log.log_type}
                    </td>
                    <td className="px-3 py-2.5">
                      <StatusPill tone={LEVEL_COLORS[log.log_level] ?? "neutral"}>
                        {log.log_level}
                      </StatusPill>
                    </td>
                    <td className="px-3 py-2.5 text-slate-300">
                      {log.operator_name || "—"}
                    </td>
                    <td className="px-3 py-2.5 text-slate-400 max-w-md truncate">
                      {log.log_content || "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </div>
  );
}
