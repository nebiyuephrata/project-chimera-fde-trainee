import type { HitlTask } from "../types/hitl";
import { confidenceTone } from "../utils/status";
import { formatRelative } from "../utils/format";

interface HitlQueueRowProps {
  task: HitlTask;
  onApprove: () => void;
  onReject: () => void;
  onEdit: () => void;
}

export default function HitlQueueRow({ task, onApprove, onReject, onEdit }: HitlQueueRowProps) {
  return (
    <tr className="border-b border-slate-800/70">
      <td className="px-4 py-4 text-sm text-slate-200">{task.task_id}</td>
      <td className="px-4 py-4 text-sm text-slate-300">{task.snippet}</td>
      <td className="px-4 py-4">
        <span className={`badge ${confidenceTone(task.confidence)}`}>
          {(task.confidence * 100).toFixed(0)}%
        </span>
      </td>
      <td className="px-4 py-4 text-sm text-slate-400">{task.reason}</td>
      <td className="px-4 py-4 text-sm text-slate-400">
        {formatRelative(task.timestamp)}
      </td>
      <td className="px-4 py-4">
        <div className="flex flex-wrap gap-2">
          <button
            className="rounded-lg bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-200"
            onClick={onApprove}
          >
            Approve
          </button>
          <button
            className="rounded-lg bg-rose-500/20 px-3 py-1 text-xs font-semibold text-rose-200"
            onClick={onReject}
          >
            Reject
          </button>
          <button
            className="rounded-lg bg-slate-500/20 px-3 py-1 text-xs font-semibold text-slate-200"
            onClick={onEdit}
          >
            Edit
          </button>
        </div>
      </td>
    </tr>
  );
}
