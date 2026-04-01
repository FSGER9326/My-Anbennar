"use client";

import { useEffect, useState } from "react";
import { BarChart3, CheckCircle2, Clock, Brain, HardDrive, Puzzle } from "lucide-react";

interface StatsData {
  tasks: {
    total: number;
    done: number;
    backlog: number;
    inProgress: number;
    review: number;
    completionRate: number;
  };
  learnings: number;
  skills: number;
  trials: number;
  memoryFiles: number;
  docFiles: number;
  uptime: number;
  memory: {
    rss: number;
    heapUsed: number;
    heapTotal: number;
  };
  model: string;
  host: string;
  channel: string;
  timezone: string;
}

function formatUptime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export default function StatsPage() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        setStats(data);
      } catch {
        // silently fail
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-gray-500 text-sm animate-pulse">Loading stats...</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-6">
        <div className="text-gray-500 text-sm">Failed to load stats</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl">
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-100">Stats</h1>
        <p className="text-xs text-gray-500 mt-0.5">Workspace overview and metrics</p>
      </div>

      <div className="space-y-6">
        {/* Task completion */}
        <section>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Tasks
          </h2>
          <div className="bg-gray-900/60 border border-gray-800/60 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-2xl font-bold text-gray-100">{stats.tasks.completionRate}%</span>
              <span className="text-xs text-gray-500">
                {stats.tasks.done} of {stats.tasks.total} completed
              </span>
            </div>
            {/* Progress bar */}
            <div className="w-full bg-gray-800 rounded-full h-2 mb-3">
              <div
                className="bg-gradient-to-r from-purple-500 to-green-500 h-2 rounded-full transition-all duration-700"
                style={{ width: `${stats.tasks.completionRate}%` }}
              />
            </div>
            {/* Breakdown */}
            <div className="grid grid-cols-4 gap-2 text-center">
              <MiniStat label="Backlog" value={stats.tasks.backlog} color="text-gray-400" />
              <MiniStat label="In Progress" value={stats.tasks.inProgress} color="text-blue-400" />
              <MiniStat label="Review" value={stats.tasks.review} color="text-yellow-400" />
              <MiniStat label="Done" value={stats.tasks.done} color="text-green-400" />
            </div>
          </div>
        </section>

        {/* Workspace metrics */}
        <section>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 flex items-center gap-1.5">
            <Brain className="w-3.5 h-3.5" /> Workspace
          </h2>
          <div className="grid grid-cols-3 gap-2">
            <MetricCard label="Learnings" value={stats.learnings} icon="📝" />
            <MetricCard label="Skills" value={stats.skills} icon="🧩" />
            <MetricCard label="Trials" value={stats.trials} icon="🔬" />
            <MetricCard label="Memory Files" value={stats.memoryFiles} icon="📁" />
            <MetricCard label="Doc Files" value={stats.docFiles} icon="📄" />
            <MetricCard label="Uptime" value={formatUptime(stats.uptime)} icon="⏱" />
          </div>
        </section>

        {/* System */}
        <section>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 flex items-center gap-1.5">
            <HardDrive className="w-3.5 h-3.5" /> System
          </h2>
          <div className="bg-gray-900/60 border border-gray-800/60 rounded-xl p-4 space-y-2">
            <DataRow label="Model" value={stats.model.split("/").pop() || stats.model} />
            <DataRow label="Host" value={stats.host} />
            <DataRow label="Channel" value={stats.channel} />
            <DataRow label="Timezone" value={stats.timezone} />
            <DataRow label="Memory (RSS)" value={`${stats.memory.rss} MB`} />
            <DataRow label="Heap Used" value={`${stats.memory.heapUsed} MB`} />
            <DataRow label="Heap Total" value={`${stats.memory.heapTotal} MB`} />
          </div>
        </section>
      </div>
    </div>
  );
}

function MiniStat({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className={`text-lg font-bold ${color}`}>{value}</div>
      <div className="text-[10px] text-gray-500">{label}</div>
    </div>
  );
}

function MetricCard({ label, value, icon }: { label: string; value: string | number; icon: string }) {
  return (
    <div className="bg-gray-900/60 border border-gray-800/60 rounded-lg px-3 py-3 text-center">
      <div className="text-lg">{icon}</div>
      <div className="text-xl font-bold text-gray-100 mt-0.5">{value}</div>
      <div className="text-[10px] text-gray-500">{label}</div>
    </div>
  );
}

function DataRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center text-xs">
      <span className="text-gray-500">{label}</span>
      <span className="text-gray-300 font-mono">{value}</span>
    </div>
  );
}
