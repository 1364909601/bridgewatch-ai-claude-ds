import { BarChart3, Download, FileText, Filter } from "lucide-react";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";

export function ReportsPage() {
  return (
    <div className="space-y-4">
      <Panel title="报告生成" eyebrow="Report Center">
        <div className="grid gap-4 md:grid-cols-3">
          {[
            {
              title: "事件统计报告",
              desc: "按类型、风险等级和时间维度统计事件数据",
              icon: BarChart3,
              color: "text-brass",
            },
            {
              title: "系统运行报告",
              desc: "系统运行状态、API 调用量和任务处理概况",
              icon: FileText,
              color: "text-signal",
            },
            {
              title: "数据导出",
              desc: "导出事件数据和统计报表为 Excel 格式",
              icon: Download,
              color: "text-blue-400",
            },
          ].map((item) => (
            <button
              key={item.title}
              type="button"
              className="group rounded-[1.5rem] border border-slate-700/50 bg-slate-900/40 p-5 text-left transition hover:border-slate-500/60 hover:bg-slate-800/40"
            >
              <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-2xl ${item.color} bg-white/5 group-hover:bg-white/10`}>
                <item.icon size={24} />
              </div>
              <h3 className="font-semibold text-white">{item.title}</h3>
              <p className="mt-2 text-sm text-slate-400">{item.desc}</p>
            </button>
          ))}
        </div>
      </Panel>

      <Panel title="最近报告" eyebrow="Recent Reports">
        <div className="space-y-3">
          {[
            { name: "2026年5月事件统计报告", date: "2026-05-13", status: "已生成" as const },
            { name: "2026年4月事件统计报告", date: "2026-04-30", status: "已生成" as const },
            { name: "2026年Q1系统运行报告", date: "2026-03-31", status: "已生成" as const },
          ].map((r) => (
            <div
              key={r.name}
              className="flex items-center justify-between rounded-xl border border-slate-700/40 bg-slate-900/30 px-4 py-3 transition hover:bg-slate-800/40"
            >
              <div className="flex items-center gap-3">
                <FileText size={18} className="text-slate-400" />
                <div>
                  <div className="text-sm font-medium text-slate-200">{r.name}</div>
                  <div className="text-xs text-slate-500">{r.date}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <StatusPill tone="ok">{r.status}</StatusPill>
                <button type="button" className="icon-button" title="下载">
                  <Download size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
