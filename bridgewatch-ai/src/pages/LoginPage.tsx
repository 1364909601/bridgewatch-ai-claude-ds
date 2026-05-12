import { Loader2, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { useAuth } from "../contexts/AuthContext";

export function LoginPage() {
  const { login, error } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) return;
    setSubmitting(true);
    setLoginError(null);
    try {
      await login(username, password);
    } catch (err: unknown) {
      setLoginError(err instanceof Error ? err.message : "登录失败");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(ellipse_at_50%_30%,rgba(26,38,35,0.9),rgb(10,12,14))] p-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-brass/20">
            <ShieldCheck size={32} className="text-brass" />
          </div>
          <h1 className="text-2xl font-semibold text-white">BridgeWatch AI</h1>
          <p className="mt-1 text-sm text-slate-400">基础设施智能监测面板</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-[1.5rem] border border-slate-700/50 bg-slate-900/60 p-6 shadow-[0_16px_48px_rgba(0,0,0,0.3)] backdrop-blur-sm"
        >
          <div className="mb-4">
            <label className="mb-1.5 block text-xs font-medium text-slate-300" htmlFor="username">
              用户名
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-800/60 px-4 py-2.5 text-sm text-white placeholder-slate-500 outline-none transition focus:border-brass/50 focus:ring-1 focus:ring-brass/30"
              placeholder="admin / operator / viewer"
              autoFocus
            />
          </div>

          <div className="mb-6">
            <label className="mb-1.5 block text-xs font-medium text-slate-300" htmlFor="password">
              密码
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-800/60 px-4 py-2.5 text-sm text-white placeholder-slate-500 outline-none transition focus:border-brass/50 focus:ring-1 focus:ring-brass/30"
              placeholder="••••••••"
            />
          </div>

          {(loginError || error) && (
            <div className="mb-4 rounded-xl bg-danger/10 px-4 py-2.5 text-sm text-danger">
              {loginError || error}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting || !username.trim() || !password.trim()}
            className="w-full rounded-xl bg-brass px-4 py-2.5 text-sm font-medium text-paper transition hover:bg-brass/90 disabled:opacity-50"
          >
            {submitting ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 size={16} className="animate-spin" />
                登录中...
              </span>
            ) : (
              "登 录"
            )}
          </button>

          <div className="mt-4 text-center text-[0.65rem] text-slate-500">
            测试账号: admin/admin123 · operator/operator123 · viewer/viewer123
          </div>
        </form>
      </div>
    </div>
  );
}
