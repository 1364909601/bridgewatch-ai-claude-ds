import { useState } from "react";
import { Loader2, Plus, ShieldCheck, Trash2, User } from "lucide-react";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";
import { useCreateUser, useDeleteUser, useUpdateUser, useUserList } from "../hooks/use-users";

export function SettingsPage() {
  const { data: usersData, isLoading } = useUserList();
  const createMutation = useCreateUser();
  const updateMutation = useUpdateUser();
  const deleteMutation = useDeleteUser();

  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ username: "", password: "", display_name: "", role: "viewer" });
  const [editingId, setEditingId] = useState<string | null>(null);

  const users = usersData?.list ?? [];

  const handleCreate = () => {
    createMutation.mutate(form, {
      onSuccess: () => {
        setShowForm(false);
        setForm({ username: "", password: "", display_name: "", role: "viewer" });
      },
    });
  };

  const handleToggleActive = (userId: string, current: boolean) => {
    updateMutation.mutate({ user_id: userId, updates: { is_active: !current } });
  };

  const handleDelete = (userId: string) => {
    if (confirm("确定要删除该用户吗？")) {
      deleteMutation.mutate(userId);
    }
  };

  const pending =
    createMutation.isPending || updateMutation.isPending || deleteMutation.isPending;

  return (
    <div className="space-y-4">
      <Panel title="用户管理" eyebrow="User Management">
        <div className="mb-4 flex items-center justify-between">
          <div className="text-sm text-slate-400">共 {users.length} 个用户</div>
          <button
            type="button"
            onClick={() => setShowForm(!showForm)}
            className="flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800/60 px-4 py-2 text-sm text-slate-200 transition hover:border-slate-400"
          >
            <Plus size={16} />
            添加用户
          </button>
        </div>

        {/* Create / Edit form */}
        {showForm && (
          <div className="mb-4 rounded-2xl border border-slate-700/50 bg-slate-900/50 p-4">
            <div className="grid gap-3 md:grid-cols-5">
              <input
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                placeholder="用户名"
                className="rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-sm text-white outline-none"
              />
              <input
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="密码"
                type="password"
                className="rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-sm text-white outline-none"
              />
              <input
                value={form.display_name}
                onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                placeholder="显示名称"
                className="rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-sm text-white outline-none"
              />
              <select
                value={form.role}
                onChange={(e) => setForm({ ...form, role: e.target.value })}
                className="rounded-xl border border-slate-700 bg-slate-800/60 px-3 py-2 text-sm text-white outline-none"
              >
                <option value="viewer">观察员</option>
                <option value="operator">操作员</option>
                <option value="admin">管理员</option>
              </select>
              <button
                type="button"
                disabled={pending || !form.username || !form.password}
                onClick={handleCreate}
                className="rounded-xl bg-brass px-3 py-2 text-sm font-medium text-paper transition hover:bg-brass/90 disabled:opacity-50"
              >
                {createMutation.isPending ? "创建中..." : "创建"}
              </button>
            </div>
          </div>
        )}

        {/* User list */}
        {isLoading ? (
          <div className="py-8 text-center text-sm text-slate-500">加载中...</div>
        ) : (
          <div className="space-y-2">
            {users.map((u) => (
              <div
                key={u.user_id}
                className="flex items-center justify-between rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-3 transition hover:bg-slate-800/40"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-brass/20">
                    <User size={18} className="text-brass" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-slate-200">{u.display_name || u.username}</span>
                      <span className="text-xs text-slate-500">@{u.username}</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                      <span>{u.role}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => handleToggleActive(u.user_id, u.is_active)}
                    disabled={pending}
                    className="text-xs"
                  >
                    <StatusPill tone={u.is_active ? "ok" : "neutral"}>
                      {u.is_active ? "启用" : "禁用"}
                    </StatusPill>
                  </button>
                  <button
                    type="button"
                    disabled={pending}
                    onClick={() => handleDelete(u.user_id)}
                    className="rounded-full border border-slate-700 bg-slate-900/60 p-2 text-slate-400 transition hover:border-danger/50 hover:text-danger"
                    title="删除"
                  >
                    {deleteMutation.isPending && deleteMutation.variables === u.user_id ? (
                      <Loader2 size={14} className="animate-spin" />
                    ) : (
                      <Trash2 size={14} />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </Panel>

      {/* ── Notification section ────────────────────────────────── */}
      <Panel title="通知设置" eyebrow="Notification">
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brass/20">
                <span className="text-sm text-brass">@</span>
              </div>
              <span className="text-sm font-medium text-slate-200">邮件通知</span>
            </div>
            <div className="mt-3 space-y-1 text-xs text-slate-500">
              <div className="flex justify-between">
                <span>SMTP 状态</span>
                <StatusPill tone="neutral">未配置</StatusPill>
              </div>
              <div className="flex justify-between">
                <span>告警推送</span>
                <span className="text-slate-400">紧急告警</span>
              </div>
              <div className="mt-2 text-slate-500">
                在 <code className="text-brass">.env</code> 中配置 SMTP_HOST、SMTP_USER、SMTP_PASSWORD 启用邮件通知
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-signal/20">
                <span className="text-sm text-signal">SMS</span>
              </div>
              <span className="text-sm font-medium text-slate-200">短信通知</span>
            </div>
            <div className="mt-3 space-y-1 text-xs text-slate-500">
              <div className="flex justify-between">
                <span>渠道状态</span>
                <StatusPill tone="neutral">待集成</StatusPill>
              </div>
              <div className="mt-2">
                短信通道可通过第三方 API 扩展（如阿里云短信、Twilio）
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/20">
                <span className="text-sm text-blue-400">🔔</span>
              </div>
              <span className="text-sm font-medium text-slate-200">页面通知</span>
            </div>
            <div className="mt-3 space-y-1 text-xs text-slate-500">
              <div className="flex justify-between">
                <span>渠道状态</span>
                <StatusPill tone="ok">已启用</StatusPill>
              </div>
              <div className="flex justify-between">
                <span>推送范围</span>
                <span className="text-slate-400">全部告警</span>
              </div>
              <div className="mt-2">
                顶部栏 Bell 组件实时显示未读告警
              </div>
            </div>
          </div>
        </div>
      </Panel>

      {/* ── Config section ──────────────────────────────────────── */}
      <div className="grid gap-4 md:grid-cols-2">
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

        <Panel title="系统信息" eyebrow="System Info">
          <div className="grid gap-4 md:grid-cols-2">
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
    </div>
  );
}
