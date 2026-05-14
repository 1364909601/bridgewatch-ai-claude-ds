import { ShieldCheck, User, Bell, Sliders } from "lucide-react";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";

export function SettingsPage() {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        <Panel title="用户管理" eyebrow="User Management">
          <div className="space-y-3">
            {[
              { name: "系统管理员", role: "admin", status: "在线" as const },
              { name: "值班操作员", role: "operator", status: "在线" as const },
              { name: "观察员", role: "viewer", status: "离线" as const },
            ].map((u) => (
              <div
                key={u.name}
                className="flex items-center justify-between rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-3"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-brass/20">
                    <User size={18} className="text-brass" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-slate-200">{u.name}</div>
                    <div className="text-xs text-slate-500">{u.role}</div>
                  </div>
                </div>
                <StatusPill tone={u.status === "在线" ? "ok" : "neutral"}>{u.status}</StatusPill>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="告警配置" eyebrow="Alert Config">
          <div className="space-y-4">
            {[
              { label: "高风险事件超时", value: "30 分钟", desc: "超过此时限自动升级告警" },
              { label: "中风险事件超时", value: "60 分钟", desc: "超过此时限自动升级告警" },
              { label: "告警轮询间隔", value: "60 秒", desc: "系统检查未复核事件的频率" },
            ].map((cfg) => (
              <div key={cfg.label} className="rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-200">{cfg.label}</span>
                  <span className="text-sm text-brass">{cfg.value}</span>
                </div>
                <div className="mt-1 text-xs text-slate-500">{cfg.desc}</div>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <Panel title="系统信息" eyebrow="System Info">
        <div className="grid gap-4 md:grid-cols-4">
          {[
            { label: "系统版本", value: "v2.0.0" },
            { label: "后端框架", value: "FastAPI" },
            { label: "数据库", value: "SQLite / PostgreSQL" },
            { label: "认证方式", value: "JWT + bcrypt" },
          ].map((info) => (
            <div key={info.label} className="rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-3 text-center">
              <div className="text-xs text-slate-500">{info.label}</div>
              <div className="mt-1 text-sm font-semibold text-slate-200">{info.value}</div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
