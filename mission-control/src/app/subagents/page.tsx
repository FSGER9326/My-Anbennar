"use client";

import { useEffect, useState } from "react";
import { Users, ChevronDown, ChevronUp, CheckCircle2, XCircle } from "lucide-react";

interface Trial {
  name: string;
  score: number;
  dimensions: Record<string, number>;
  scope: string;
  lesson: string;
  status: "completed" | "failed" | "running";
}

const statusConfig = {
  completed: { color: "bg-green-500", textColor: "text-green-400", label: "Completed" },
  failed: { color: "bg-red-500", textColor: "text-red-400", label: "Failed" },
  running: { color: "bg-blue-500 animate-pulse-dot", textColor: "text-blue-400", label: "Running" },
};

function scoreColor(score: number): string {
  if (score >= 4) return "text-green-400";
  if (score === 3) return "text-yellow-400";
  return "text-red-400";
}

export default function SubagentsPage() {
  const [trials, setTrials] = useState<Trial[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const [filter, setFilter] = useState<"all" | "completed" | "failed">("all");

  useEffect(() => {
    const fetchTrials = async () => {
      try {
        const res = await fetch("/api/subagents");
        const data = await res.json();
        setTrials(data);
      } catch {
        // silently fail
      } finally {
        setLoading(false);
      }
    };
    fetchTrials();
    const interval = setInterval(fetchTrials, 30000);
    return () => clearInterval(interval);
  }, []);

  const filtered = filter === "all" ? trials : trials.filter((t) => t.status === filter);

  const completedCount = trials.filter((t) => t.status === "completed").length;
  const failedCount = trials.filter((t) => t.status === "failed").length;
  const avgScore = trials.length > 0
    ? (trials.reduce((s, t) => s + t.score, 0) / trials.length).toFixed(1)
    : "—";

  const toggle = (name: string) => {
    setExpanded((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  return (
    <div className="p-6 max-w-3xl">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-100">Subagents</h1>
        <p className="text-xs text-gray-500 mt-0.5">
          {trials.length} trials · {completedCount} completed · {failedCount} failed · avg score {avgScore}
        </p>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1 mb-4">
        {(["all", "completed", "failed"] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              filter === f
                ? "bg-purple-500/15 text-purple-400"
                : "text-gray-500 hover:text-gray-300 hover:bg-gray-800/40"
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-gray-500 text-sm animate-pulse">Loading subagents...</div>
      ) : filtered.length === 0 ? (
        <div className="text-gray-500 text-sm text-center py-12">
          {filter === "all" ? "No trials recorded yet" : `No ${filter} trials`}
        </div>
      ) : (
        <div className="space-y-1.5">
          {filtered.map((trial, i) => {
            const isOpen = expanded[trial.name] || false;
            const sc = statusConfig[trial.status];
            const dimEntries = Object.entries(trial.dimensions);

            return (
              <div
                key={i}
                className="bg-gray-900/60 border border-gray-800/60 rounded-lg overflow-hidden hover:border-gray-700/60 transition-colors"
              >
                {/* Row header */}
                <button
                  onClick={() => toggle(trial.name)}
                  className="w-full flex items-center gap-3 px-4 py-3 text-left"
                >
                  {/* Status dot */}
                  <div className={`w-2 h-2 rounded-full ${sc.color} shrink-0`} />

                  {/* Name */}
                  <div className="flex-1 min-w-0">
                    <span className="text-sm text-gray-200 font-medium truncate block">
                      {trial.name}
                    </span>
                  </div>

                  {/* Scope */}
                  <span className="text-[10px] text-gray-500 bg-gray-800 px-1.5 py-0.5 rounded hidden sm:block">
                    {trial.scope}
                  </span>

                  {/* Score badge */}
                  <span className={`text-sm font-bold ${scoreColor(trial.score)}`}>
                    {trial.score}/5
                  </span>

                  {/* Status */}
                  <span className={`text-[10px] ${sc.textColor} font-medium`}>
                    {sc.label}
                  </span>

                  {/* Expand icon */}
                  {isOpen ? (
                    <ChevronUp className="w-3.5 h-3.5 text-gray-600" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-gray-600" />
                  )}
                </button>

                {/* Expanded detail */}
                {isOpen && (
                  <div className="px-4 pb-3 border-t border-gray-800/40">
                    {/* Dimension scores */}
                    <div className="flex flex-wrap gap-2 mt-3 mb-3">
                      {dimEntries.map(([key, val]) => (
                        <div
                          key={key}
                          className="flex items-center gap-1.5 bg-gray-950 rounded-md px-2 py-1.5"
                        >
                          <span className="text-[10px] text-gray-500">{key}</span>
                          <span className={`text-xs font-bold ${scoreColor(val)}`}>{val}</span>
                        </div>
                      ))}
                    </div>

                    {/* Lesson */}
                    {trial.lesson && (
                      <div className="bg-gray-950 rounded-md px-3 py-2">
                        <div className="text-[10px] text-gray-500 uppercase mb-0.5">Lesson</div>
                        <p className="text-xs text-gray-300">{trial.lesson}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
