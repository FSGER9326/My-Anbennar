"use client";

import { useEffect, useState } from "react";
import { Activity, GitCommit, Bot, User, Terminal, FileText } from "lucide-react";

interface ActivityEntry {
  timestamp: string;
  type: "system" | "task" | "subagent" | "user" | "file";
  message: string;
  source?: string;
}

const typeConfig: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
  system: { icon: <Terminal className="w-3.5 h-3.5" />, color: "text-gray-400", label: "System" },
  task: { icon: <GitCommit className="w-3.5 h-3.5" />, color: "text-blue-400", label: "Task" },
  subagent: { icon: <Bot className="w-3.5 h-3.5" />, color: "text-purple-400", label: "Subagent" },
  user: { icon: <User className="w-3.5 h-3.5" />, color: "text-green-400", label: "User" },
  file: { icon: <FileText className="w-3.5 h-3.5" />, color: "text-yellow-400", label: "File" },
};

function formatTimestamp(ts: string): string {
  try {
    const d = new Date(ts);
    return d.toLocaleString("de-DE", {
      timeZone: "Europe/Berlin",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

function formatDate(ts: string): string {
  try {
    const d = new Date(ts);
    return d.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  } catch {
    return ts;
  }
}

export default function ActivityPage() {
  const [entries, setEntries] = useState<ActivityEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const res = await fetch("/api/activity");
        const data = await res.json();
        setEntries(data);
      } catch {
        // silently fail
      } finally {
        setLoading(false);
      }
    };
    fetchActivity();
    const interval = setInterval(fetchActivity, 30000);
    return () => clearInterval(interval);
  }, []);

  const filtered = filter === "all" ? entries : entries.filter((e) => e.type === filter);

  // Group by date
  const grouped: Record<string, ActivityEntry[]> = {};
  for (const entry of filtered) {
    const dateKey = formatDate(entry.timestamp);
    if (!grouped[dateKey]) grouped[dateKey] = [];
    grouped[dateKey].push(entry);
  }

  const types = ["all", "system", "task", "subagent", "user", "file"];

  return (
    <div className="p-6 max-w-3xl">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-gray-100">Activity Log</h1>
        <p className="text-xs text-gray-500 mt-0.5">
          {entries.length} events
        </p>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1 mb-5 flex-wrap">
        {types.map((t) => (
          <button
            key={t}
            onClick={() => setFilter(t)}
            className={`flex items-center gap-1 px-3 py-1 text-xs rounded-md transition-colors ${
              filter === t
                ? "bg-purple-500/15 text-purple-400"
                : "text-gray-500 hover:text-gray-300 hover:bg-gray-800/40"
            }`}
          >
            {t !== "all" && typeConfig[t]?.icon}
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-gray-500 text-sm animate-pulse">Loading activity...</div>
      ) : filtered.length === 0 ? (
        <div className="text-gray-500 text-sm text-center py-12">No activity</div>
      ) : (
        <div className="space-y-6">
          {Object.entries(grouped).map(([date, dateEntries]) => (
            <div key={date}>
              <div className="text-[10px] text-gray-600 uppercase font-medium mb-2">{date}</div>
              <div className="space-y-0.5">
                {dateEntries.map((entry, i) => {
                  const tc = typeConfig[entry.type] || typeConfig.system;
                  return (
                    <div
                      key={i}
                      className="flex items-start gap-3 px-3 py-2 rounded-lg hover:bg-gray-900/40 transition-colors group"
                    >
                      {/* Timeline dot + line */}
                      <div className="flex flex-col items-center mt-0.5">
                        <div className={`w-1.5 h-1.5 rounded-full bg-gray-600 group-hover:bg-purple-500 transition-colors`} />
                      </div>

                      {/* Icon */}
                      <div className={`${tc.color} mt-0.5 shrink-0`}>
                        {tc.icon}
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-300 leading-snug">{entry.message}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <span className="text-[10px] text-gray-600">{tc.label}</span>
                          {entry.source && (
                            <>
                              <span className="text-[10px] text-gray-700">·</span>
                              <span className="text-[10px] text-gray-600">{entry.source}</span>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Timestamp */}
                      <span className="text-[10px] text-gray-600 shrink-0 tabular-nums">
                        {formatTimestamp(entry.timestamp).split(" ").pop()}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
