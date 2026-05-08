import { motion } from "framer-motion";
import { modelVersions, taskRuns } from "../data/mockData";
import { Panel } from "../components/Panel";
import { StatusPill } from "../components/StatusPill";

function statusTone(status: string) {
  if (status === "失败") return "danger";
  if (status === "运行中" || status === "在线") return "ok";
  if (status === "验证中") return "warning";
  return "neutral";
}

export function ModelOpsPage() {
  return (
    <div className="grid gap-4 xl:grid-cols-[0.95fr_1.05fr]">
      <Panel title="模型版本矩阵" eyebrow="Release Matrix">
        <div className="space-y-3">
          {modelVersions.map((model, index) => (
            <motion.div
              key={model.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="rounded-[1.2rem] border border-slate-700 bg-slate-950/35 p-4"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="font-medium text-white">{model.name}</div>
                  <div className="mt-1 text-sm text-slate-400">{model.scope}</div>
                </div>
                <StatusPill tone={statusTone(model.status)}>{model.status}</StatusPill>
              </div>
              <div className="mt-4 flex items-center justify-between font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                <span>{model.version}</span>
                <span>{model.updatedAt}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </Panel>

      <Panel title="任务执行面板" eyebrow="Inference Queue">
        <div className="space-y-3">
          {taskRuns.map((task) => (
            <div key={task.name} className="rounded-[1.2rem] border border-slate-700 bg-slate-950/35 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="font-medium text-white">{task.name}</div>
                  <div className="mt-1 text-sm text-slate-400">开始于 {task.startedAt} / ETA {task.eta}</div>
                </div>
                <StatusPill tone={statusTone(task.status)}>{task.status}</StatusPill>
              </div>
              <div className="mt-4 h-2 rounded-full bg-slate-800">
                <div
                  className={`h-2 rounded-full ${task.status === "失败" ? "bg-[#d15b57]" : task.status === "成功" ? "bg-[#4e8d78]" : "bg-[#d3914d]"}`}
                  style={{ width: `${task.progress}%` }}
                />
              </div>
              <div className="mt-3 font-mono text-xs uppercase tracking-[0.18em] text-slate-500">Progress {task.progress}%</div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}
