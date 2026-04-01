"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Plus,
  Activity,
  GitCommit,
  Bot,
  User,
  Terminal,
  FileText,
  ArrowRight,
  GripVertical,
  Info,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

// ─── Types ──────────────────────────────────────────────

interface Task {
  id: string;
  title: string;
  description: string;
  status: "backlog" | "in-progress" | "review" | "done";
  priority: number;
  assignee: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

interface ActivityEntry {
  timestamp: string;
  type: "system" | "task" | "subagent" | "user" | "file";
  message: string;
  source?: string;
}

interface ColumnDef {
  key: Task["status"];
  label: string;
  accent: string;
  dotColor: string;
}

// ─── Config ─────────────────────────────────────────────

const columns: ColumnDef[] = [
  { key: "backlog", label: "Backlog", accent: "border-gray-600", dotColor: "bg-gray-500" },
  { key: "in-progress", label: "In Progress", accent: "border-blue-500/50", dotColor: "bg-blue-500" },
  { key: "review", label: "Review", accent: "border-yellow-500/50", dotColor: "bg-yellow-500" },
  { key: "done", label: "Done", accent: "border-green-500/50", dotColor: "bg-green-500" },
];

const priorityDot: Record<number, string> = {
  1: "bg-red-500",
  2: "bg-orange-500",
  3: "bg-yellow-500",
  4: "bg-blue-500",
  5: "bg-purple-500",
};

const priorityLabel: Record<number, string> = {
  1: "Critical",
  2: "High",
  3: "Medium",
  4: "Low",
  5: "Backlog",
};

const assigneeDisplay: Record<string, { emoji: string; label: string }> = {
  jordan: { emoji: "🟣", label: "Jordan" },
  falk: { emoji: "🔵", label: "Falk" },
  "subagent-auto": { emoji: "🤖", label: "Auto" },
  "subagent-qa": { emoji: "🤖", label: "QA" },
  "subagent-audit": { emoji: "🤖", label: "Audit" },
  "subagent-wiki": { emoji: "🤖", label: "Wiki" },
  "subagent-inspire": { emoji: "🤖", label: "Inspire" },
  "subagent-sync": { emoji: "🤖", label: "Sync" },
  "subagent-bg": { emoji: "🤖", label: "BgWorker" },
};

const typeConfig: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
  system: { icon: <Terminal className="w-3 h-3" />, color: "text-gray-400", label: "System" },
  task: { icon: <GitCommit className="w-3 h-3" />, color: "text-blue-400", label: "Task" },
  subagent: { icon: <Bot className="w-3 h-3" />, color: "text-purple-400", label: "Subagent" },
  user: { icon: <User className="w-3 h-3" />, color: "text-green-400", label: "User" },
  file: { icon: <FileText className="w-3 h-3" />, color: "text-yellow-400", label: "File" },
};

// ─── Helpers ────────────────────────────────────────────

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  return `${days}d`;
}

function formatActivityTime(ts: string): string {
  try {
    const d = new Date(ts);
    return d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

const statusOrder: Task["status"][] = ["backlog", "in-progress", "review", "done"];

// ─── Main Component ─────────────────────────────────────

export default function OverviewPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activity, setActivity] = useState<ActivityEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewTask, setShowNewTask] = useState(false);
  const [dragId, setDragId] = useState<string | null>(null);
  const [dragOverCol, setDragOverCol] = useState<string | null>(null);
  const [legendOpen, setLegendOpen] = useState(true);
  const [activityFilter, setActivityFilter] = useState("all");
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskPriority, setNewTaskPriority] = useState(1);
  const [continuousWork, setContinuousWork] = useState(false);
  const [cwStartedAt, setCwStartedAt] = useState<string | null>(null);
  const [cwCurrentTask, setCwCurrentTask] = useState<string | null>(null);
  const [cwCompleted, setCwCompleted] = useState(0);

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    try {
      const res = await fetch("/api/tasks");
      setTasks(await res.json());
    } catch {}
  }, []);

  // Fetch activity
  const fetchActivity = useCallback(async () => {
    try {
      const res = await fetch("/api/activity");
      setActivity(await res.json());
    } catch {}
  }, []);

  useEffect(() => {
    fetchTasks();
    fetchActivity();
    const interval = setInterval(() => {
      fetchTasks();
      fetchActivity();
    }, 30000);
    return () => clearInterval(interval);
  }, [fetchTasks, fetchActivity]);
  useEffect(() => {
    setLoading(false);
  }, []);

  // Fetch continuous work state
  useEffect(() => {
    fetch("/api/continuous-work")
      .then((r) => r.json())
      .then((d) => {
        setContinuousWork(d.active || false);
        setCwStartedAt(d.startedAt || null);
        setCwCurrentTask(d.currentTask || null);
        setCwCompleted(d.tasksCompleted || 0);
      })
      .catch(() => {});
  }, []);

  // Toggle continuous work
  const toggleContinuousWork = async () => {
    const newState = !continuousWork;
    setContinuousWork(newState);
    if (!newState) {
      setCwStartedAt(null);
      setCwCurrentTask(null);
    }
    try {
      await fetch("/api/continuous-work", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ active: newState }),
      });
    } catch {}
  };

  // Move task (drag & drop or button)
  const moveTask = async (id: string, newStatus: Task["status"]) => {
    setTasks((prev) =>
      prev.map((t) =>
        t.id === id ? { ...t, status: newStatus, updatedAt: new Date().toISOString() } : t
      )
    );
    try {
      await fetch("/api/tasks", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, status: newStatus }),
      });
      // If moved to in-progress, log activity
      if (newStatus === "in-progress") {
        fetchActivity();
      }
    } catch {
      fetchTasks();
    }
  };

  // Drag handlers
  const handleDragStart = (id: string) => setDragId(id);
  const handleDragOver = (e: React.DragEvent, colKey: string) => {
    e.preventDefault();
    setDragOverCol(colKey);
  };
  const handleDrop = (colKey: Task["status"]) => {
    if (dragId) moveTask(dragId, colKey);
    setDragId(null);
    setDragOverCol(null);
  };
  const handleDragEnd = () => {
    setDragId(null);
    setDragOverCol(null);
  };

  // Create new task
  const createTask = async () => {
    if (!newTaskTitle.trim()) return;
    const task = {
      id: `task-${Date.now()}`,
      title: newTaskTitle.trim(),
      description: "",
      status: "backlog" as const,
      priority: newTaskPriority,
      assignee: "jordan",
      tags: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setTasks((prev) => [...prev, task]);
    setShowNewTask(false);
    setNewTaskTitle("");
    setNewTaskPriority(1);
    try {
      await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(task),
      });
    } catch {}
  };

  // Computed
  const tasksByStatus = (s: Task["status"]) => tasks.filter((t) => t.status === s);
  const counts = Object.fromEntries(columns.map((c) => [c.key, tasksByStatus(c.key).length]));
  const filteredActivity =
    activityFilter === "all" ? activity : activity.filter((e) => e.type === activityFilter);

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="px-6 py-3 border-b border-gray-800/60 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-lg font-semibold text-gray-100">Overview</h1>
            <p className="text-xs text-gray-500 mt-0.5">
              {tasks.length} tasks · {counts["done"] || 0} done
            </p>
          </div>
          {/* Status summary pills */}
          {columns.map((c) => (
            <div
              key={c.key}
              className={`flex items-center gap-1.5 px-2 py-1 rounded-md text-[11px] font-medium ${
                c.key === "backlog"
                  ? "bg-gray-800/60 text-gray-400"
                  : c.key === "in-progress"
                  ? "bg-blue-500/10 text-blue-400"
                  : c.key === "review"
                  ? "bg-yellow-500/10 text-yellow-400"
                  : "bg-green-500/10 text-green-400"
              }`}
            >
              <div className={`w-1.5 h-1.5 rounded-full ${c.dotColor}`} />
              {counts[c.key] || 0} {c.label}
            </div>
          ))}
        </div>
        <div className="flex items-center gap-3">
          {/* Continuous Work Toggle */}
          <button
            onClick={toggleContinuousWork}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              continuousWork
                ? "bg-green-500/15 text-green-400 ring-1 ring-green-500/30 animate-pulse"
                : "bg-gray-800/60 text-gray-400 hover:bg-gray-700/60 hover:text-gray-300"
            }`}
            title={continuousWork ? "Continuous Work is ON — click to stop" : "Start continuous autonomous work"}
          >
            <div className={`w-2 h-2 rounded-full ${continuousWork ? "bg-green-400 animate-ping" : "bg-gray-600"}`} />
            {continuousWork ? "Working..." : "Start Work"}
          </button>
          <button
            onClick={() => setShowNewTask(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            New Task
          </button>
        </div>
      </div>

      {/* Continuous Work Status Bar */}
      {continuousWork && (
        <div className="px-6 py-2 bg-green-500/5 border-b border-green-500/20 flex items-center gap-4 shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs font-medium text-green-400">Continuous Work Active</span>
          </div>
          {cwCurrentTask && (
            <span className="text-xs text-green-300/60">
              Working on: {cwCurrentTask}
            </span>
          )}
          {cwCompleted > 0 && (
            <span className="text-xs text-green-300/40">
              {cwCompleted} tasks completed
            </span>
          )}
          <span className="text-[10px] text-green-300/30 ml-auto">
            Click "Working..." to pause
          </span>
        </div>
      )}

      {/* New Task Inline Form */}
      {showNewTask && (
        <div className="px-6 py-3 bg-gray-900/80 border-b border-gray-800/60 flex items-center gap-3 shrink-0">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Task title..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-md px-3 py-1.5 text-sm text-gray-200 placeholder:text-gray-500 focus:outline-none focus:border-purple-500"
            autoFocus
            onKeyDown={(e) => e.key === "Enter" && createTask()}
          />
          <select
            value={newTaskPriority}
            onChange={(e) => setNewTaskPriority(Number(e.target.value))}
            className="bg-gray-800 border border-gray-700 rounded-md px-2 py-1.5 text-sm text-gray-300 focus:outline-none"
          >
            {[1, 2, 3, 4, 5].map((p) => (
              <option key={p} value={p}>
                {priorityLabel[p]}
              </option>
            ))}
          </select>
          <button
            onClick={createTask}
            className="px-3 py-1.5 bg-purple-600 hover:bg-purple-700 text-white text-xs font-medium rounded-md"
          >
            Create
          </button>
          <button
            onClick={() => setShowNewTask(false)}
            className="px-3 py-1.5 text-gray-400 text-xs hover:text-gray-300"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Legend */}
      <div className="px-6 py-2 bg-gray-900/40 border-b border-gray-800/40 shrink-0">
        <button
          onClick={() => setLegendOpen(!legendOpen)}
          className="flex items-center gap-1.5 text-[10px] text-gray-500 hover:text-gray-400"
        >
          <Info className="w-3 h-3" />
          Priority Legend
          {legendOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
        </button>
        {legendOpen && (
          <div className="flex items-center gap-4 mt-1.5">
            {Object.entries(priorityLabel).map(([p, label]) => (
              <div key={p} className="flex items-center gap-1.5">
                <div className={`w-2 h-2 rounded-full ${priorityDot[Number(p)]}`} />
                <span className="text-[10px] text-gray-500">{label}</span>
              </div>
            ))}
            <span className="text-[10px] text-gray-600 ml-2">
              · Drag cards between columns or use the ⋯ menu
            </span>
          </div>
        )}
      </div>

      {/* Main Content: Kanban + Activity */}
      <div className="flex-1 flex overflow-hidden">
        {/* Kanban Board */}
        <div className="flex-1 overflow-auto p-4">
          {loading ? (
            <div className="text-gray-500 text-sm animate-pulse p-4">Loading...</div>
          ) : (
            <div className="grid grid-cols-4 gap-3 min-h-0">
              {columns.map((col) => (
                <div
                  key={col.key}
                  onDragOver={(e) => handleDragOver(e, col.key)}
                  onDrop={() => handleDrop(col.key)}
                  onDragLeave={() => setDragOverCol(null)}
                  className={`flex flex-col min-h-0 rounded-lg transition-all ${
                    dragOverCol === col.key
                      ? "bg-purple-500/5 ring-1 ring-purple-500/30"
                      : "bg-transparent"
                  }`}
                >
                  {/* Column header */}
                  <div
                    className={`flex items-center justify-between px-2 pb-2 mb-2 border-b ${col.accent}`}
                  >
                    <div className="flex items-center gap-1.5">
                      <div className={`w-2 h-2 rounded-full ${col.dotColor}`} />
                      <span className="text-[11px] font-semibold text-gray-400 uppercase tracking-wide">
                        {col.label}
                      </span>
                    </div>
                    <span className="text-[10px] text-gray-600 bg-gray-800 rounded-full w-5 h-5 flex items-center justify-center font-medium">
                      {counts[col.key] || 0}
                    </span>
                  </div>

                  {/* Cards */}
                  <div className="flex-1 space-y-1.5 overflow-y-auto pr-1 pb-2">
                    {tasksByStatus(col.key).map((task) => {
                      const assignee = assigneeDisplay[task.assignee] || {
                        emoji: "🟣",
                        label: task.assignee,
                      };
                      const currentIdx = statusOrder.indexOf(task.status);

                      return (
                        <div
                          key={task.id}
                          draggable
                          onDragStart={() => handleDragStart(task.id)}
                          onDragEnd={handleDragEnd}
                          className={`group relative bg-gray-900/80 border rounded-lg px-3 py-2.5 transition-all duration-150 cursor-grab active:cursor-grabbing ${
                            dragId === task.id
                              ? "opacity-30 scale-95 border-purple-500/50"
                              : "border-gray-800/60 hover:border-gray-700"
                          }`}
                        >
                          {/* Drag handle */}
                          <div className="absolute left-0 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-40 transition-opacity">
                            <GripVertical className="w-3 h-3 text-gray-600" />
                          </div>

                          {/* Priority + Title */}
                          <div className="flex items-start gap-2">
                            <div
                              className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                                priorityDot[task.priority] || "bg-gray-600"
                              }`}
                            />
                            <div className="min-w-0 flex-1">
                              <div className="text-[13px] text-gray-200 font-medium leading-snug">
                                {task.title}
                              </div>
                              {task.description && (
                                <div className="text-[11px] text-gray-500 mt-0.5 line-clamp-1">
                                  {task.description}
                                </div>
                              )}
                            </div>

                            {/* Move menu */}
                            <div className="relative opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                              <button className="p-0.5 text-gray-600 hover:text-gray-300">⋯</button>
                              <div className="hidden group-focus-within:block absolute right-0 top-6 z-10 bg-gray-800 border border-gray-700 rounded-lg shadow-xl py-1 min-w-[130px]">
                                {currentIdx > 0 && (
                                  <button
                                    onClick={() =>
                                      moveTask(task.id, statusOrder[currentIdx - 1])
                                    }
                                    className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-gray-300 hover:bg-gray-700/50"
                                  >
                                    ← {columns[currentIdx - 1].label}
                                  </button>
                                )}
                                {currentIdx < statusOrder.length - 1 && (
                                  <button
                                    onClick={() =>
                                      moveTask(task.id, statusOrder[currentIdx + 1])
                                    }
                                    className="flex items-center gap-2 w-full px-3 py-1.5 text-xs text-gray-300 hover:bg-gray-700/50"
                                  >
                                    <ArrowRight className="w-3 h-3" />
                                    {columns[currentIdx + 1].label}
                                  </button>
                                )}
                              </div>
                            </div>
                          </div>

                          {/* Meta */}
                          <div className="flex items-center gap-2 mt-2 ml-4 flex-wrap">
                            <span className="text-[10px] text-gray-500">
                              {assignee.emoji} {assignee.label}
                            </span>
                            <span className="text-[10px] text-gray-600">·</span>
                            <span className="text-[10px] text-gray-500">
                              {timeAgo(task.updatedAt)} ago
                            </span>
                            {task.tags.slice(0, 2).map((tag) => (
                              <span
                                key={tag}
                                className="text-[10px] px-1.5 py-0.5 rounded bg-gray-800 text-gray-500"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                      );
                    })}
                    {tasksByStatus(col.key).length === 0 && (
                      <div
                        className={`text-[11px] text-center py-8 rounded-lg border border-dashed transition-colors ${
                          dragOverCol === col.key
                            ? "border-purple-500/30 text-purple-400 bg-purple-500/5"
                            : "border-gray-800/40 text-gray-700"
                        }`}
                      >
                        {dragOverCol === col.key ? "Drop here" : "No tasks"}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Activity Feed (right sidebar) */}
        <div className="w-72 border-l border-gray-800/60 bg-gray-950 flex flex-col shrink-0">
          <div className="px-3 py-2.5 border-b border-gray-800/60 flex items-center gap-2">
            <Activity className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-xs font-medium text-gray-400">Live Feed</span>
            <span className="text-[10px] text-gray-600 ml-auto">{activity.length}</span>
          </div>
          {/* Filter pills */}
          <div className="px-3 py-2 border-b border-gray-800/40 flex gap-1 flex-wrap">
            {["all", "task", "subagent", "system"].map((t) => (
              <button
                key={t}
                onClick={() => setActivityFilter(t)}
                className={`px-2 py-0.5 text-[10px] rounded-md transition-colors ${
                  activityFilter === t
                    ? "bg-purple-500/15 text-purple-400"
                    : "text-gray-500 hover:text-gray-300 hover:bg-gray-800/40"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
          {/* Feed */}
          <div className="flex-1 overflow-y-auto">
            {filteredActivity.length === 0 ? (
              <div className="text-gray-600 text-xs text-center py-8">No activity</div>
            ) : (
              filteredActivity.slice(0, 50).map((entry, i) => {
                const tc = typeConfig[entry.type] || typeConfig.system;
                return (
                  <div
                    key={i}
                    className="flex items-start gap-2 px-3 py-2 hover:bg-gray-900/40 transition-colors border-b border-gray-800/20"
                  >
                    <div className={`${tc.color} mt-0.5 shrink-0`}>{tc.icon}</div>
                    <div className="flex-1 min-w-0">
                      <p className="text-[11px] text-gray-400 leading-snug line-clamp-2">
                        {entry.message}
                      </p>
                    </div>
                    <span className="text-[9px] text-gray-600 shrink-0 tabular-nums mt-0.5">
                      {formatActivityTime(entry.timestamp)}
                    </span>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
