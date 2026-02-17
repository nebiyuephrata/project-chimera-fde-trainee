import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";
import HitlQueueRow from "../components/HitlQueueRow";
import { useHitlWebSocket } from "../hooks/useHitlWebSocket";
import { checkHitlHealth, fetchHitlQueue, updateHitlTask } from "../services/hitlApi";
import type { HitlState } from "../context/hitlStore";
import { useHitlStore } from "../context/hitlStore";

const WS_URL = "ws://localhost:8000/hitl";

export default function HITLQueuePage() {
  const { status, reconnect } = useHitlWebSocket(WS_URL);
  const tasks = useHitlStore((state: HitlState) => state.tasks);
  const setTasks = useHitlStore((state: HitlState) => state.setTasks);
  const updateStatus = useHitlStore((state: HitlState) => state.updateStatus);
  const [apiHealthy, setApiHealthy] = useState(true);
  const pendingCount = tasks.filter((task) => task.status === "pending").length;

  const { data, isLoading, isError } = useQuery({
    queryKey: ["hitl-queue"],
    queryFn: fetchHitlQueue,
  });

  useEffect(() => {
    if (data) {
      setTasks(data);
    }
  }, [data, setTasks]);

  useEffect(() => {
    checkHitlHealth()
      .then(setApiHealthy)
      .catch(() => setApiHealthy(false));
  }, []);

  return (
    <div className="min-h-screen grid-glow">
      <main className="mx-auto max-w-6xl px-6 py-12">
        <header className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-slate-400">
              Chimera / HITL
            </p>
            <h1 className="mt-2 font-display text-4xl text-fog md:text-5xl">
              Review Queue
            </h1>
            <p className="mt-3 max-w-xl text-slate-300">
              Human-in-the-loop moderation for low-confidence agent outputs.
            </p>
          </div>
          <div className="card px-6 py-4">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
              WebSocket
            </p>
            <div className="mt-2 flex items-center gap-3 text-sm">
              <span
                className={`h-2 w-2 rounded-full ${
                  status === "open"
                    ? "bg-emerald-400"
                    : status === "connecting"
                    ? "bg-yellow-400"
                    : "bg-rose-400"
                }`}
              />
              <span className="text-slate-200">{status}</span>
              {(status === "error" || status === "closed") && (
                <button
                  className="ml-2 text-xs font-semibold text-emerald-300"
                  onClick={reconnect}
                >
                  Retry
                </button>
              )}
            </div>
            {!apiHealthy && (
              <p className="mt-2 text-xs text-rose-300">
                API offline. Start `make -f infra/Makefile api`.
              </p>
            )}
          </div>
          <div className="card px-6 py-4">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
              Pending
            </p>
            <p className="mt-2 text-2xl font-display text-fog">{pendingCount}</p>
          </div>
        </header>

        <section className="mt-10 card p-6">
          <div className="flex items-center justify-between">
            <h2 className="font-display text-2xl text-fog">Queue</h2>
            <span className="text-sm text-slate-400">
              {tasks.length} tasks awaiting review
            </span>
          </div>

          {isLoading && (
            <div className="mt-6 grid gap-3">
              {Array.from({ length: 3 }).map((_, index) => (
                <div
                  key={`skeleton-${index}`}
                  className="h-14 rounded-xl bg-slate-800/60"
                />
              ))}
            </div>
          )}

          {isError && (
            <div className="mt-6 rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 text-sm text-rose-200">
              Unable to load the initial queue. Verify the HITL API is running.
            </div>
          )}

          {!isLoading && tasks.length > 0 && (
            <div className="mt-6 overflow-x-auto">
              <table className="w-full border-collapse text-left text-sm">
                <thead className="text-xs uppercase text-slate-400">
                  <tr>
                    <th className="px-4 py-3">Task</th>
                    <th className="px-4 py-3">Snippet</th>
                    <th className="px-4 py-3">Confidence</th>
                    <th className="px-4 py-3">Reason</th>
                    <th className="px-4 py-3">Timestamp</th>
                    <th className="px-4 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {tasks.map((task) => (
                    <HitlQueueRow
                      key={task.task_id}
                      task={task}
                      onApprove={async () => {
                        try {
                          const updated = await updateHitlTask(task.task_id, "approve");
                          updateStatus(updated.task_id, updated.status);
                        } catch {
                          toast.error("Approve failed. API unavailable.");
                        }
                      }}
                      onReject={async () => {
                        try {
                          const updated = await updateHitlTask(task.task_id, "reject");
                          updateStatus(updated.task_id, updated.status);
                        } catch {
                          toast.error("Reject failed. API unavailable.");
                        }
                      }}
                      onEdit={async () => {
                        try {
                          const updated = await updateHitlTask(task.task_id, "edit");
                          updateStatus(updated.task_id, updated.status);
                        } catch {
                          toast.error("Edit failed. API unavailable.");
                        }
                      }}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
