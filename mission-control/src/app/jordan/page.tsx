"use client";

import { useEffect, useState } from "react";
import { Bot, Clock, Brain, HardDrive, CheckCircle2, Zap } from "lucide-react";

interface AgentInfo {
  name: string;
  status: string;
  model: string;
  channel: string;
  sessionStart: string;
  timezone: string;
  host: string;
  uptime: number;
  memory: {
    rss: number;
    heapUsed: number;
    heapTotal: number;
  };
  stats: {
    learningsCount: number;
    skillsCount: number;
    memoryFiles: number;
    workspaceFiles: number;
    totalTasks: number;
    doneTasks: number;
  };
  recentDecisions: string[];
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatUptime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export default function JordanPage() {
  const [info, setInfo] = useState<AgentInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const fetchAgent = async () => {
      try {
        const res = await fetch("/api/agent");
        const data = await res.json();
        setInfo(data);
      } catch {
        // silently fail
      } finally {
        setLoading(false);
      }
    };
    fetchAgent();
    const interval = setInterval(fetchAgent, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const memPct = info?.memory
    ? Math.round((info.memory.heapUsed / info.memory.heapTotal) * 100)
    : 0;

  return (
    <div className="p-6 max-w-2xl">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <div className="w-14 h-14 rounded-2xl bg-purple-600 flex items-center justify-center">
          <Bot className="w-7 h-7 text-white" />
        </div>
        <div>
          <h1 className="text-xl font-semibold text-gray-100">Jordan</h1>
          <div className="flex items-center gap-2 mt-1">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-dot" />
            <span className="text-sm text-gray-400">{info?.status || "idle"}</span>
            <span className="text-gray-600">·</span>
            <span className="text-xs text-gray-500">
              Session started {info ? formatUptime(now.getTime() / 1000 - (now.getTime() - new Date(info.sessionStart).getTime()) / 1000) : "..."} ago
            </span>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-gray-500 text-sm animate-pulse">Loading agent info...</div>
      ) : info ? (
        <div className="space-y-6">
          {/* System info */}
          <section>
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
              System
            </h2>
            <div className="grid grid-cols-2 gap-2">
              <InfoTile label="Model" value={info.model.split("/").pop() || info.model} icon={<Zap className="w-3.5 h-3.5" />} />
              <InfoTile label="Channel" value={info.channel} icon={<Clock className="w-3.5 h-3.5" />} />
              <InfoTile label="Host" value={info.host} icon={<HardDrive className="w-3.5 h-3.5" />} />
              <InfoTile label="Timezone" value={info.timezone} icon={<Clock className="w-3.5 h-3.5" />} />
            </div>
          </section>

          {/* Memory */}
          <section>
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Memory Usage
            </h2>
            <div className="bg-gray-900/60 border border-gray-800/60 rounded-lg p-3">
              <div className="flex justify-between text-xs mb-2">
                <span className="text-gray-400">Heap</span>
                <span className="text-gray-500">
                  {formatBytes(info.memory.heapUsed)} / {formatBytes(info.memory.heapTotal)}
                </span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-1.5">
                <div
                  className={`h-1.5 rounded-full transition-all duration-500 ${
                    memPct > 80 ? "bg-red-500" : memPct > 60 ? "bg-yellow-500" : "bg-green-500"
                  }`}
                  style={{ width: `${memPct}%` }}
                />
              </div>
              <div className="text-[10px] text-gray-600 mt-1 text-right">{memPct}%</div>
            </div>
          </section>

          {/* Stats */}
          <section>
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Workspace Stats
            </h2>
            <div className="grid grid-cols-3 gap-2">
              <StatBox label="Tasks" value={`${info.stats.doneTasks}/${info.stats.totalTasks}`} sub="completed" />
              <StatBox label="Learnings" value={String(info.stats.learningsCount)} sub="entries" />
              <StatBox label="Skills" value={String(info.stats.skillsCount)} sub="installed" />
              <StatBox label="Memory Files" value={String(info.stats.memoryFiles)} sub="daily notes" />
              <StatBox label="Doc Files" value={String(info.stats.workspaceFiles)} sub="in docs/" />
              <StatBox label="Uptime" value={formatUptime(info.uptime)} sub="this session" />
            </div>
          </section>

          {/* Recent Decisions */}
          <section>
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Recent Decisions
            </h2>
            <div className="space-y-1.5">
              {info.recentDecisions.map((decision, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 bg-gray-900/40 border border-gray-800/40 rounded-lg px-3 py-2"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-purple-400 mt-0.5 shrink-0" />
                  <span className="text-sm text-gray-300">{decision}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      ) : (
        <div className="text-gray-500 text-sm">Failed to load agent info</div>
      )}
    </div>
  );
}

function InfoTile({ label, value, icon }: { label: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-gray-900/60 border border-gray-800/60 rounded-lg px-3 py-2.5">
      <div className="flex items-center gap-1 text-[10px] uppercase text-gray-500 mb-0.5">
        {icon} {label}
      </div>
      <div className="text-sm text-gray-200 font-medium truncate">{value}</div>
    </div>
  );
}

function StatBox({ label, value, sub }: { label: string; value: string; sub: string }) {
  return (
    <div className="bg-gray-900/60 border border-gray-800/60 rounded-lg px-3 py-2.5 text-center">
      <div className="text-lg font-bold text-gray-100">{value}</div>
      <div className="text-[10px] text-gray-500">{label}</div>
    </div>
  );
}
