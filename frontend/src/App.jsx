import { useEffect, useState } from "react";

const statusColors = {
  online: "text-emerald-400",
  busy: "text-amber-400",
  offline: "text-rose-400",
};

export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/api/status.json")
      .then((res) => res.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  const fleet = data?.fleet;

  return (
    <div className="min-h-screen grid-glow">
      <main className="mx-auto max-w-6xl px-6 py-12">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
              Project Chimera
            </p>
            <h1 className="mt-2 font-display text-4xl text-fog md:text-5xl">
              Fleet Dashboard
            </h1>
            <p className="mt-2 max-w-xl text-slate-300">
              Live snapshot of agents, queues, and orchestration health for the
              autonomous influencer network.
            </p>
          </div>
          <div className="card px-6 py-4 shadow-glow">
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
              Last Sync
            </p>
            <p className="mt-2 text-lg text-fog">
              {fleet?.last_sync ?? "Awaiting status"}
            </p>
          </div>
        </header>

        <section className="mt-10 grid gap-6 md:grid-cols-4">
          <div className="card p-6">
            <p className="text-sm text-slate-400">Agents</p>
            <p className="mt-3 text-3xl font-display text-fog">
              {fleet?.agents ?? "--"}
            </p>
          </div>
          <div className="card p-6">
            <p className="text-sm text-slate-400">Active Now</p>
            <p className="mt-3 text-3xl font-display text-fog">
              {fleet?.active ?? "--"}
            </p>
          </div>
          <div className="card p-6">
            <p className="text-sm text-slate-400">Queued Tasks</p>
            <p className="mt-3 text-3xl font-display text-fog">
              {fleet?.queued_tasks ?? "--"}
            </p>
          </div>
          <div className="card p-6">
            <p className="text-sm text-slate-400">Wallet Balance</p>
            <p className="mt-3 text-3xl font-display text-fog">
              {fleet?.wallet_balance ?? "--"}
            </p>
          </div>
        </section>

        <section className="mt-10">
          <div className="flex items-center justify-between">
            <h2 className="font-display text-2xl text-fog">Agents</h2>
            <span className="text-sm text-slate-400">
              {data?.agents?.length ?? 0} units tracked
            </span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            {(data?.agents ?? []).map((agent) => (
              <div key={agent.id} className="card p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-display text-lg text-fog">{agent.id}</p>
                    <p className="text-sm text-slate-400">
                      Last task: {agent.last_task}
                    </p>
                  </div>
                  <span
                    className={`text-sm font-semibold ${
                      statusColors[agent.status] ?? "text-slate-400"
                    }`}
                  >
                    {agent.status}
                  </span>
                </div>
              </div>
            ))}
            {!data && (
              <div className="card p-6 text-slate-300">
                Status feed unavailable. Check `frontend/public/api/status.json`.
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
